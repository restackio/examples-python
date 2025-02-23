
from dataclasses import dataclass
import os
from livekit import api 
from livekit.protocol.sip import CreateSIPParticipantRequest, SIPParticipantInfo
from restack_ai.function import function, log, FunctionFailure

@dataclass
class LivekitCallInput:
    sip_trunk_id: str
    phone_number: str
    room_id: str
    agent_name: str
    agent_id: str
    run_id: str


@function.defn()
async def livekit_call(function_input: LivekitCallInput) -> SIPParticipantInfo:
  
  try:
      livekit_api = api.LiveKitAPI()

      request = CreateSIPParticipantRequest(
        sip_trunk_id = function_input.sip_trunk_id,
        sip_call_to = function_input.phone_number,
        room_name = function_input.room_id,
        participant_identity = function_input.agent_id,
        participant_name = function_input.agent_name,
        play_dialtone = True
      )

      log.info("livekit_call CreateSIPParticipantRequest: ", request=request)

      participant = await livekit_api.sip.create_sip_participant(request)
      
      await livekit_api.aclose()

      log.info("livekit_call SIPParticipantInfo:", participant=participant)

      return participant

  except Exception as e:
    log.error("livekit_call function failed", error=str(e))
    raise FunctionFailure(f"livekit_call function failed: {str(e)}", non_retryable=True)


