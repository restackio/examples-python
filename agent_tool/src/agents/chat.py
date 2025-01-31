from datetime import timedelta
import json
from typing import List
from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log
from src.workflows.workflow import SalesWorkflow

with import_functions():
    from src.functions.llm_chat import llm_chat, LlmChatInput, Message

class MessageEvent(BaseModel):
    content: str

class EndEvent(BaseModel):
    end: bool

@workflow.defn()
class AgentChat:
    def __init__(self) -> None:
        self.end = False
        self.messages = []

    @workflow.event
    async def message(self, message: MessageEvent) -> List[Message]:
        log.info(f"Received message: {message.content}")

        self.messages.append(Message(role="user", content=message.content or ""))
        completion = await workflow.step(llm_chat, LlmChatInput(messages=self.messages), start_to_close_timeout=timedelta(seconds=120))

        log.info(f"completion: {completion}")
        
        tool_calls = completion.choices[0].message.tool_calls
        self.messages.append(Message(role="assistant", content=completion.choices[0].message.content or "", tool_calls=tool_calls))

        log.info(f"tool_calls: {tool_calls}")

        for tool_call in tool_calls:
          log.info(f"tool_call: {tool_call}")

          name = tool_call.function.name
          args = json.loads(tool_call.function.arguments)

          match name:
            case SalesWorkflow.__name__:
              log.info(f"calling {name} with args: {args}")

              result = await workflow.child_execute(SalesWorkflow, workflow_id=tool_call.id, input=args)
              self.messages.append(Message(role="tool", tool_call_id=tool_call.id, content=str(result)))

              completion_with_tool_call = await workflow.step(llm_chat, LlmChatInput(messages=self.messages), start_to_close_timeout=timedelta(seconds=120))
              self.messages.append(Message(role="assistant", content=completion_with_tool_call.choices[0].message.content or ""))
              
        return self.messages
    
    @workflow.event
    async def end(self, end: EndEvent) -> EndEvent:
        log.info(f"Received end")
        self.end = True
        return end
  
    @workflow.run
    async def run(self, input: dict):
        await workflow.condition(
            lambda: self.end
        )
        return


