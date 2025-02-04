from dataclasses import dataclass
from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import FunctionInputParams, openai_greet


@dataclass
class WorkflowInputParams:
    name: str


@workflow.defn()
class OpenaiGreetWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("OpenaiGreetWorkflow started", input=input)
        user_content = f"Greet this person {input.name}"

        greet_message = await workflow.step(
            openai_greet,
            FunctionInputParams(
                user_content=user_content,
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("OpenaiGreetWorkflow completed", greet_message=greet_message)
        return greet_message
