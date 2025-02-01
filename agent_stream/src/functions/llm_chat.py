from ..client import api_address
from restack_ai.function import function, log, function_info, heartbeat
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import os
from pydantic import BaseModel
from typing import Literal, Optional, List
import websockets

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class LlmChatInput(BaseModel):
    system_content: Optional[str] = None
    model: Optional[str] = None
    messages: Optional[List[Message]] = None

@function.defn()
async def llm_chat(input: LlmChatInput) -> str:
    try:
        workflow_id = function_info().workflow_id
        run_id = function_info().workflow_run_id

        log.info("llm_chat function started", input=input)
        client = OpenAI(base_url="https://ai.restack.io", api_key=os.environ.get("RESTACK_API_KEY"))

        if input.system_content:
            input.messages.append({"role": "system", "content": input.system_content})

        # Initialize a list to collect the messages
        collected_messages = []

        # Create a WebSocket connection
        websocket_url = f"ws://{api_address}/ws?workflowId={workflow_id}&runId={run_id}"
        async with websockets.connect(websocket_url) as websocket:
            try:
                
                info = {
                    "activityId": function_info().activity_id,
                    "workflowId": function_info().workflow_id,
                    "runId": function_info().workflow_run_id,
                    "activityType": function_info().activity_type,
                    "taskQueue": function_info().task_queue,
                }
                # Send initial message
                await websocket.send(str(info))
                heartbeat(info)

                # Get the streamed response from OpenAI API
                response:ChatCompletion = client.chat.completions.create(
                    model=input.model or "restack-c1",
                    messages=input.messages,
                    stream=True,
                )

                # Iterate over the streamed response and send each chunk to WebSocket
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    collected_messages.append(content)
                    if chunk.choices[0].delta:
                      chunkInfo = {
                          **info,
                          "chunk": chunk.__dict__
                      }
                      log.info("sending content to websocket", chunkInfo=chunkInfo)
                      heartbeat(chunkInfo)
                      await websocket.send(str(chunkInfo))

                collected_messages = [m for m in collected_messages if m is not None]
                final_response = ''.join(collected_messages)

                log.info("llm_chat function completed", final_response=final_response)
                return str(final_response)  # Modify the return type if necessary

            finally:
                # Ensure the WebSocket connection is closed
                await websocket.close()

    except Exception as e:
        log.error("llm_chat function failed", error=e)
        raise e
