from restack_ai.workflow import workflow, workflow_import
from pydantic import BaseModel, Field
from datetime import timedelta

with workflow_import():
    from src.functions.function import openai_greet, FunctionInputParams

class WorkflowInputParams(BaseModel):
    name: str

class MessageSchema(BaseModel):
    message: str = Field(..., description="The message to greet the person")

# This workflow uses the OpenAI function to greet a person
@workflow.defn(name="OpenaiGreetWorkflow")
class OpenaiGreetWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        user_content = f"Greet this person {input.name}"

        message_schema=MessageSchema(message=user_content)

        json_schema={
            "name": "greet",
            "description": "Greet a person",
            "parameters": message_schema.model_json_schema()
        }

        openai_output = await workflow.step(openai_greet, FunctionInputParams(user_content=user_content, message_schema=json_schema), start_to_close_timeout=timedelta(seconds=10))
        print(openai_output)
        greet_message = openai_output.choices[0].message.content
        return greet_message