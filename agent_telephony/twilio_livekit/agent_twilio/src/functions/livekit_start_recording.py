import os

from livekit import api
from livekit.api import (
    EgressInfo,
    EncodedFileType,
    RoomCompositeEgressRequest,
)
from pydantic import BaseModel
from restack_ai.function import NonRetryableError, function, log


class LivekitStartRecordingInput(BaseModel):
    room_id: str

class LivekitStartRecordingOutput(BaseModel):
    recording_url: str
    egress_info: EgressInfo

@function(
    name="livekit_start_recording",
    description="Start a recording of the call",
)
async def livekit_start_recording(function_input: LivekitStartRecordingInput) -> LivekitStartRecordingOutput:
    try:
        if os.getenv("GCP_CREDENTIALS") is None:
            raise NonRetryableError(
                message="GCP_CREDENTIALS is not set"
            )

        credentials = os.getenv("GCP_CREDENTIALS")
        log.info("GCP_CREDENTIALS", credentials=credentials)

        lkapi = api.LiveKitAPI(
            url=os.getenv("LIVEKIT_API_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET"),
        )

        recording = await lkapi.egress.start_room_composite_egress(
            RoomCompositeEgressRequest(
                room_name=function_input.room_id,
                layout="grid",
                audio_only=True,
                file_outputs=[
                    api.EncodedFileOutput(
                        file_type=EncodedFileType.MP4,
                        filepath=f"{function_input.room_id}-audio.mp4",
                        gcp=api.GCPUpload(
                            credentials=credentials,
                            bucket="livekit-local-recordings",
                        ),
                    )
                ],
            )
        )

        recording_url = f"https://storage.googleapis.com/{recording.room_composite.file_outputs[0].gcp.bucket}/{recording.room_composite.file_outputs[0].filepath}"

        await lkapi.aclose()

    except Exception as e:
        error_message = (
            f"livekit_start_recording function failed: {e}"
        )
        raise NonRetryableError(error_message) from e

    else:
        return LivekitStartRecordingOutput(
            recording_url=recording_url,
            egress_info=recording.egress_info
        )
