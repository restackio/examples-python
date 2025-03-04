import os
from dataclasses import dataclass

from restack_ai.function import NonRetryableError, function, log
from vapi import AsyncVapi, Call


@dataclass
class VapiCallInput:
    assistant_id: str
    phone_number: str


@function.defn()
async def vapi_call(function_input: VapiCallInput) -> Call:
    try:
        client = AsyncVapi(
            token=os.getenv("VAPI_TOKEN"),
        )

        call = await client.calls.create(
            assistant_id=function_input.assistant_id,
            phone_number_id=function_input.phone_number,
        )

        log.info("vapi_call: ", call=call)

    except Exception as e:
        error_message = f"vapi_call function failed: {e}"
        raise NonRetryableError(error_message) from e
    else:
        return call
