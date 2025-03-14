import asyncio
import base64
import json
import os
import uuid

import aiohttp
import websockets
from livekit import rtc
from livekit.rtc._proto.video_frame_pb2 import VideoBufferType
from loguru import logger
from pipecat.audio.utils import create_default_resampler
from pipecat.frames.frames import (
    CancelFrame,
    EndFrame,
    ErrorFrame,
    Frame,
    OutputImageRawFrame,
    StartFrame,
    TTSAudioRawFrame,
    TTSStartedFrame,
    TTSStoppedFrame,
    StartInterruptionFrame,
)
from pipecat.processors.frame_processor import FrameDirection
from pipecat.services.ai_services import AIService


class HeyGenVideoService(AIService):
    """Class to send agent audio to HeyGen using the streaming audio input api."""

    def __init__(
        self,
        *,
        session_id: str,
        session_token: str,
        realtime_endpoint: str,
        session: aiohttp.ClientSession,
        livekit_room_url: str,
        api_base_url: str = "https://api.heygen.com",
        **kwargs: dict,
    ) -> None:
        super().__init__(**kwargs)
        self._session_id = session_id
        self._session_token = session_token
        self._session = session
        self._api_base_url = api_base_url
        self._websocket = None
        self._buffered_audio_duration_ms = 0
        self._event_id = None
        self._realtime_endpoint = realtime_endpoint
        self._livekit_room_url = livekit_room_url
        self._livekit_room = None
        self._video_task = None
        self._audio_task = None
        self._video_event = asyncio.Event()
        self._video_event.set()

    # Constants
    SAMPLE_RATE = 24000
    BUFFER_DURATION_THRESHOLD_MS = 20
    BUFFER_COMMIT_THRESHOLD_MS = 200

    # AI Service class methods
    async def start(self, frame: StartFrame) -> None:
        logger.info("HeyGenVideoService starting")
        await super().start(frame)
        await self._ws_connect()
        await self._livekit_connect()

    async def stop(self, frame: EndFrame) -> None:
        logger.info("HeyGenVideoService stopping")
        await super().stop(frame)
        await self._stop()

    async def cancel(self, frame: CancelFrame) -> None:
        logger.info("HeyGenVideoService canceling")
        await super().cancel(frame)
        await self._ws_disconnect()
        await self._livekit_disconnect()
        await self.stop_ttfb_metrics()
        await self.stop_processing_metrics()
      
    async def interrupt(self, frame: StartInterruptionFrame) -> None:
        logger.info("HeyGenVideoService interrupting")
        await super().interrupt(frame)
        await self._interrupt()

    # websocket connection methods
    async def _ws_connect(self) -> None:
        """Connect to HeyGen websocket endpoint."""
        try:
            logger.info("HeyGenVideoService ws connecting")
            if self._websocket:
                # assume connected
                return
            self._websocket = await websockets.connect(
                uri=self._realtime_endpoint,
            )
            self._receive_task = (
                self.get_event_loop().create_task(
                    self._ws_receive_task_handler(),
                )
            )
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"{self} initialization error: {e}")
            self._websocket = None

    async def _ws_disconnect(self) -> None:
        """Disconnect from HeyGen websocket endpoint."""
        try:
            if self._websocket:
                await self._websocket.close()
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"{self} disconnect error: {e}")
        finally:
            self._websocket = None

    async def _ws_receive_task_handler(self) -> None:
        """Handle incoming messages from HeyGen websocket."""
        try:
            while True:
                message = await self._websocket.recv()
                try:
                    parsed_message = json.loads(message)
                    await self._handle_ws_server_event(
                        parsed_message,
                    )
                except json.JSONDecodeError as e:
                    logger.error(
                        f"Failed to parse websocket message as JSON: {e}",
                    )
                    continue
                if message:
                    logger.info(
                        f"HeyGenVideoService ws received message: {message}",
                    )

        except websockets.exceptions.WebSocketException as e:
            logger.error(
                f"Error receiving message from websocket: {e}",
            )

    async def _handle_ws_server_event(self, event: dict) -> None:
        """Handle an event from HeyGen websocket."""
        event_type = event.get("type")
        if event_type == "agent.state":
            logger.info(
                f"HeyGenVideoService ws received agent state: {event}",
            )
        else:
            logger.error(
                f"HeyGenVideoService ws received unknown event: {event_type}",
            )

    async def _ws_send(self, message: dict) -> None:
        """Send a message to HeyGen websocket."""
        try:
            # logger.debug(
            #     f"HeyGenVideoService ws sending message: {message.get('type')}",
            # )
            if self._websocket:
                await self._websocket.send(json.dumps(message))
            else:
                logger.error(f"{self} websocket not connected")
        except websockets.exceptions.WebSocketException as e:
            logger.error(
                f"Error sending message to websocket: {e}",
            )
            await self.push_error(
                ErrorFrame(
                    error=f"Error sending client event: {e}",
                    fatal=True,
                ),
            )

    async def _stop_session(self) -> None:
        """Stop the current session."""
        try:
            await self._ws_disconnect()
        except websockets.exceptions.WebSocketException as e:
            logger.error(f"{self} stop ws error: {e}")
        url = f"{self._api_base_url}/v1/streaming.stop"
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "x-api-key": os.getenv("HEYGEN_API_KEY"),
        }
        body = {"session_id": self._session_id}
        async with self._session.post(
            url,
            headers=headers,
            json=body,
        ) as r:
            r.raise_for_status()

    async def _interrupt(self) -> None:
        """Interrupt the current session."""
        url = f"{self._api_base_url}/v1/streaming.interrupt"
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "x-api-key": os.getenv("HEYGEN_API_KEY"),
        }
        body = {"session_id": self._session_id}
        async with self._session.post(
            url,
            headers=headers,
            json=body,
        ) as r:
            r.raise_for_status()
    # audio buffer methods
    async def _send_audio(
        self,
        audio: bytes,
        sample_rate: int,
        event_id: str,
        finish: bool = False,
    ) -> None:
        try:
            if sample_rate != self.SAMPLE_RATE:
                resampler = create_default_resampler()
                audio = await resampler.resample(
                    audio,
                    sample_rate,
                    self.SAMPLE_RATE,
                )
            # If sample_rate is already 16000, no resampling is needed
            self._buffered_audio_duration_ms += (
                self._calculate_audio_duration_ms(
                    audio,
                    self.SAMPLE_RATE,
                )
            )
            await self._agent_audio_buffer_append(audio)

            if (
                finish
                and self._buffered_audio_duration_ms
                < self.BUFFER_DURATION_THRESHOLD_MS
            ):
                await self._agent_audio_buffer_clear()
                self._buffered_audio_duration_ms = 0

            if (
                finish
                or self._buffered_audio_duration_ms
                > self.BUFFER_COMMIT_THRESHOLD_MS
            ):
                logger.info(
                    f"Audio buffer duration from buffer: {self._buffered_audio_duration_ms:.2f}ms",
                )
                await self._agent_audio_buffer_commit()
                self._buffered_audio_duration_ms = 0
        except Exception as e:
            logger.error(
                f"Error sending audio: {e}",
                exc_info=True,
            )

    def _calculate_audio_duration_ms(
        self,
        audio: bytes,
        sample_rate: int,
    ) -> float:
        # Each sample is 2 bytes (16-bit audio)
        num_samples = len(audio) / 2
        return (num_samples / sample_rate) * 1000

    async def _agent_audio_buffer_append(
        self,
        audio: bytes,
    ) -> None:
        audio_base64 = base64.b64encode(audio).decode("utf-8")
        await self._ws_send(
            {
                "type": "agent.audio_buffer_append",
                "audio": audio_base64,
                "event_id": str(uuid.uuid4()),
            },
        )

    async def _agent_audio_buffer_clear(self) -> None:
        await self._ws_send(
            {
                "type": "agent.audio_buffer_clear",
                "event_id": str(uuid.uuid4()),
            },
        )

    async def _agent_audio_buffer_commit(self) -> None:
        audio_base64 = base64.b64encode(b"\x00").decode("utf-8")
        await self._ws_send(
            {
                "type": "agent.audio_buffer_commit",
                "audio": audio_base64,
                "event_id": str(uuid.uuid4()),
            },
        )

    # LiveKit connection methods
    async def _process_audio_frames(
        self,
        stream: rtc.AudioStream,
    ) -> None:
        """Process audio frames from LiveKit stream."""
        frame_count = 0
        try:
            logger.info("Starting audio frame processing...")
            async for frame_event in stream:
                frame_count += 1
                try:
                    audio_frame = frame_event.frame
                    # Convert audio to raw bytes
                    audio_data = bytes(audio_frame.data)

                    # Create TTSAudioRawFrame
                    audio_frame = TTSAudioRawFrame(
                        audio=audio_data,
                        sample_rate=audio_frame.sample_rate,
                        num_channels=1,  # HeyGen uses mono audio
                    )
                    # Mark this frame as coming from LiveKit to avoid reprocessing

                    await self.push_frame(audio_frame)

                except Exception as frame_error:
                    logger.error(
                        f"Error processing audio frame #{frame_count}: {frame_error!s}",
                        exc_info=True,
                    )
        except Exception as e:
            logger.error(
                f"Audio frame processing error after {frame_count} frames: {e!s}",
                exc_info=True,
            )
        finally:
            logger.info(
                f"Audio frame processing ended. Total frames processed: {frame_count}",
            )

    async def _process_video_frames(
        self,
        stream: rtc.VideoStream,
    ) -> None:
        """Process video frames from LiveKit stream."""
        frame_count = 0
        try:
            logger.info("Starting video frame processing...")
            async for frame_event in stream:
                # Wait for video processing to be enabled
                await self._video_event.wait()

                frame_count += 1
                try:
                    video_frame = frame_event.frame

                    # Convert to RGB24 if not already
                    if video_frame.type != VideoBufferType.RGB24:
                        video_frame = video_frame.convert(
                            VideoBufferType.RGB24,
                        )

                    # Create frame with original dimensions
                    image_frame = OutputImageRawFrame(
                        image=bytes(video_frame.data),
                        size=(
                            video_frame.width,
                            video_frame.height,
                        ),
                        format="RGB",
                    )
                    image_frame.pts = (
                        frame_event.timestamp_us // 1000
                    )  # Convert to milliseconds

                    await self.push_frame(image_frame)

                except Exception as frame_error:
                    logger.error(
                        f"Error processing individual frame #{frame_count}: {frame_error!s}",
                        exc_info=True,
                    )
        except Exception as e:
            logger.error(
                f"Video frame processing error after {frame_count} frames: {e!s}",
                exc_info=True,
            )
        finally:
            logger.info(
                f"Video frame processing ended. Total frames processed: {frame_count}",
            )

    async def _livekit_connect(self) -> None:
        """Connect to LiveKit room."""
        try:
            logger.info(
                f"HeyGenVideoService livekit connecting to room URL: {self._livekit_room_url}",
            )
            self._livekit_room = rtc.Room()

            @self._livekit_room.on("participant_connected")
            def on_participant_connected(
                participant: rtc.RemoteParticipant,
            ) -> None:
                logger.info(
                    f"Participant connected - SID: {participant.sid}, Identity: {participant.identity}",
                )
                for (
                    track_pub
                ) in participant.track_publications.values():
                    logger.info(
                        f"Available track - SID: {track_pub.sid}, Kind: {track_pub.kind}, Name: {track_pub.name}",
                    )

            @self._livekit_room.on("track_subscribed")
            def on_track_subscribed(
                track: rtc.Track,
                publication: rtc.RemoteTrackPublication,
            ) -> None:
                logger.info(
                    f"Track subscribed - SID: {publication.sid}, Kind: {track.kind}, Source: {publication.source}",
                )
                if track.kind == rtc.TrackKind.KIND_VIDEO:
                    logger.info(
                        f"Creating video stream processor for track: {publication.sid}",
                    )
                    video_stream = rtc.VideoStream(track)
                    self._video_task = self.create_task(
                        self._process_video_frames(video_stream),
                    )
                elif track.kind == rtc.TrackKind.KIND_AUDIO:
                    logger.info(
                        f"Creating audio stream processor for track: {publication.sid}",
                    )
                    audio_stream = rtc.AudioStream(track)
                    self._audio_task = self.create_task(
                        self._process_audio_frames(audio_stream),
                    )

            @self._livekit_room.on("track_unsubscribed")
            def on_track_unsubscribed(
                track: rtc.Track,
                publication: rtc.RemoteTrackPublication,
            ) -> None:
                logger.info(
                    f"Track unsubscribed - SID: {publication.sid}, Kind: {track.kind}",
                )

            @self._livekit_room.on("participant_disconnected")
            def on_participant_disconnected(
                participant: rtc.RemoteParticipant,
            ) -> None:
                logger.info(
                    f"Participant disconnected - SID: {participant.sid}, Identity: {participant.identity}",
                )

            logger.info(
                "Attempting to connect to LiveKit room...",
            )
            await self._livekit_room.connect(
                self._livekit_room_url,
                self._session_token,
            )
            logger.info(
                f"Successfully connected to LiveKit room: {self._livekit_room.name}",
            )

            # Log initial room state
            logger.info(f"Room name: {self._livekit_room.name}")
            logger.info(
                f"Local participant SID: {self._livekit_room.local_participant.sid}",
            )
            logger.info(
                f"Number of remote participants: {len(self._livekit_room.remote_participants)}",
            )

            # Log existing participants and their tracks
            for (
                participant
            ) in self._livekit_room.remote_participants.values():
                logger.info(
                    f"Existing participant - SID: {participant.sid}, Identity: {participant.identity}",
                )
                for (
                    track_pub
                ) in participant.track_publications.values():
                    logger.info(
                        f"Existing track - SID: {track_pub.sid}, Kind: {track_pub.kind}, Name: {track_pub.name}",
                    )

        except Exception as e:
            logger.error(
                f"LiveKit initialization error: {e!s}",
                exc_info=True,
            )
            self._livekit_room = None

    async def _livekit_disconnect(self) -> None:
        """Disconnect from LiveKit room."""
        try:
            logger.info("Starting LiveKit disconnect...")
            if self._video_task:
                logger.info("Canceling video processing task")
                await self.cancel_task(self._video_task)
                self._video_task = None
                logger.info(
                    "Video processing task cancelled successfully",
                )

            if self._audio_task:
                logger.info("Canceling audio processing task")
                await self.cancel_task(self._audio_task)
                self._audio_task = None
                logger.info(
                    "Audio processing task cancelled successfully",
                )

            if self._livekit_room:
                logger.info("Disconnecting from LiveKit room")
                await self._livekit_room.disconnect()
                self._livekit_room = None
                logger.info(
                    "Successfully disconnected from LiveKit room",
                )
        except Exception as e:
            logger.error(
                f"LiveKit disconnect error: {e!s}",
                exc_info=True,
            )

    async def _stop(self) -> None:
        """Stop all processing and disconnect."""
        if self._video_task:
            await self.cancel_task(self._video_task)
            self._video_task = None
        if self._audio_task:
            await self.cancel_task(self._audio_task)
            self._audio_task = None

        await self._ws_disconnect()
        await self._livekit_disconnect()
        await self._stop_session()

    async def process_frame(
        self,
        frame: Frame,
        direction: FrameDirection,
    ) -> None:
        await super().process_frame(frame, direction)
        try:
            if isinstance(frame, TTSStartedFrame):
                logger.info("HeyGenVideoService TTS started")
                await self.start_processing_metrics()
                await self.start_ttfb_metrics()
                self._event_id = str(uuid.uuid4())
                await self._agent_audio_buffer_clear()
            elif isinstance(frame, TTSAudioRawFrame):
                await self._send_audio(
                    frame.audio,
                    frame.sample_rate,
                    self._event_id,
                    finish=False,
                )
                await self.stop_ttfb_metrics()
            elif isinstance(frame, TTSStoppedFrame):
                logger.info("HeyGenVideoService TTS stopped")
                await self._send_audio(
                    b"\x00\x00",
                    self.SAMPLE_RATE,
                    self._event_id,
                    finish=True,
                )
                await self.stop_processing_metrics()
                self._event_id = None
            elif isinstance(frame, StartInterruptionFrame):
                await self._interrupt()
            elif isinstance(frame, EndFrame | CancelFrame):
                logger.info("HeyGenVideoService session ended")
                await self._stop()
            else:
                await self.push_frame(frame, direction)
        except Exception as e:
            logger.error(
                f"Error processing frame: {e}",
                exc_info=True,
            )
