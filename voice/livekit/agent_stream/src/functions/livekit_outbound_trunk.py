import os
from livekit import api 
from restack_ai.function import function, log, FunctionFailure, function_info
from livekit.protocol.sip import CreateSIPOutboundTrunkRequest, SIPOutboundTrunkInfo, ListSIPOutboundTrunkRequest


@function.defn()
async def livekit_outbound_trunk() -> str:
  
  try:
      livekit_api = api.LiveKitAPI()
      run_id = function_info().workflow_run_id

      existing_trunk = await livekit_api.sip.list_sip_outbound_trunk(
          list=ListSIPOutboundTrunkRequest(trunk_ids=[str(run_id)])
      )

      if existing_trunk.items and len(existing_trunk.items) > 0:
          first_trunk = existing_trunk.items[0]
          if first_trunk.sip_trunk_id:
              log.info("livekit_outbound_trunk Trunk already exists: ", trunk_id=first_trunk.sip_trunk_id)
              return first_trunk.sip_trunk_id

      trunk = SIPOutboundTrunkInfo(
          name = run_id,
          address = os.getenv('LIVEKIT_SIP_ADDRESS'),
          numbers = [os.getenv('TWILIO_PHONE_NUMBER')],
          auth_username = os.getenv('TWILIO_TRUNK_AUTH_USERNAME'),
          auth_password = os.getenv('TWILIO_TRUNK_AUTH_PASSWORD')
      )

      request = CreateSIPOutboundTrunkRequest(trunk=trunk)

      trunk = await livekit_api.sip.create_sip_outbound_trunk(request)

      log.info("livekit_outbound_trunk Successfully created, trunk: ", trunk=trunk)

      await livekit_api.aclose()

      return trunk.sip_trunk_id

  except Exception as e:
      log.error("livekit_outbound_trunk function failed", error=str(e))
      raise FunctionFailure(f"livekit_outbound_trunk function failed: {str(e)}", non_retryable=True)


