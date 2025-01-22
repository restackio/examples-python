from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions
import json

with import_functions():
    from src.functions.e2b_execute_python import e2b_execute_python, ExecutePythonInput
    from src.functions.openai_tool_call import openai_tool_call, OpenaiToolCallInput

class CodeExecutionWorkflowInput(BaseModel):
    user_content: str = Field(default='Calculate how many r\'s are in the word \'strawberry\'')
    system_content: str = Field(default='You are an expert in Python. You can execute Python code and return the result.')

class CodeExecutionWorkflowOutput(BaseModel):
    content: str

@workflow.defn()
class CodeExecutionWorkflow:
    @workflow.run
    async def run(self, input: CodeExecutionWorkflowInput) -> CodeExecutionWorkflowOutput:

        messages = []
        while True:
            llm_response = await workflow.step(openai_tool_call, input=OpenaiToolCallInput(
                model="gpt-4o-mini",
                user_content=input.user_content if not messages else None,
                system_content=input.system_content if not messages else None,
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "execute_python",
                        "description": "Execute python code in a Jupyter notebook cell and return result",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "code": {"type": "string", "description": "The python code to execute"}
                            },
                            "required": ["code"]
                        }
                    }
                }] if not messages else []
            ))

            messages = llm_response["messages"]
            
            if not llm_response["response"].get("tool_calls"):
                return CodeExecutionWorkflowOutput(content=llm_response["response"].get("content"))
                
            tool_call = llm_response["response"]["tool_calls"][0]
            code = json.loads(tool_call["function"]["arguments"])["code"]
            code_execution_output = await workflow.step(e2b_execute_python, input=ExecutePythonInput(code=code))

            messages.append({
                "role": "tool",
                "name": "execute_python",
                "content": str(code_execution_output),
                "tool_call_id": tool_call["id"]
            })