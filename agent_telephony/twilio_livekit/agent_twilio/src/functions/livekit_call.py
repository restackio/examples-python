from dataclasses import dataclass

from livekit import api
from livekit.protocol.sip import (
    CreateSIPParticipantRequest,
    SIPParticipantInfo,
)
from restack_ai.function import NonRetryableError, function, log


@dataclass
class LivekitCallInput:
    sip_trunk_id: str
    phone_number: str
    room_id: str
    agent_name: str
    agent_id: str
    run_id: str


@function.defn()
async def livekit_call(
    function_input: LivekitCallInput,
) -> SIPParticipantInfo:
    try:
        livekit_api = api.LiveKitAPI()

        request = CreateSIPParticipantRequest(
            sip_trunk_id=function_input.sip_trunk_id,
            sip_call_to=function_input.phone_number,
            room_name=function_input.room_id,
            participant_identity=function_input.agent_id,
            participant_name=function_input.agent_name,
            play_dialtone=True,
        )

        log.info(
            "livekit_call CreateSIPParticipantRequest: ",
            request=request,
        )

        participant = (
            await livekit_api.sip.create_sip_participant(request)
        )

        await livekit_api.aclose()

        log.info(
            "livekit_call SIPParticipantInfo:",
            participant=participant,
        )
    except Exception as e:
        error_message = f"livekit_call function failed: {e}"
        raise NonRetryableError(error_message) from e
    else:
        return participant
