from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import ExampleFunctionInput, example_function
    from src.functions.synthesize import SynthesizeInputParams, lmnt_synthesize


class ChildWorkflowInput(BaseModel):
    name: str = Field(default="Hi John Doe")
    voice: str = Field(default="morgan")


@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(
        self,
        child_workflow_input: ChildWorkflowInput,
    ) -> dict[str, str]:
        log.info("ChildWorkflow started")
        await workflow.step(
            example_function,
            input=ExampleFunctionInput(name=child_workflow_input.name),
            start_to_close_timeout=timedelta(minutes=2),
        )

        await workflow.sleep(1)

        audiofile_path = await workflow.step(
            lmnt_synthesize,
            SynthesizeInputParams(
                user_content=child_workflow_input.name,
                voice=child_workflow_input.voice,
                filename=f"{child_workflow_input.voice.lower().replace(' ', '_')}.mp3",
            ),
            task_queue="lmnt",
            start_to_close_timeout=timedelta(minutes=2),
        )

        return {
            "audiofile_path": audiofile_path,
        }
