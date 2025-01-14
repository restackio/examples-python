from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.synthesize import lmnt_synthesize, SynthesizeInputParams
    from src.functions.function import example_function, ExampleFunctionInput

class ChildWorkflowInput(BaseModel):
    name: str = Field(default='Hi John Doe')
    voice: str = Field(default='morgan')

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: ChildWorkflowInput):
        log.info("ChildWorkflow started")
        await workflow.step(example_function, input=ExampleFunctionInput(name=input.name), start_to_close_timeout=timedelta(minutes=2))

        await workflow.sleep(1)

        audiofile_path = await workflow.step(
            lmnt_synthesize,
            SynthesizeInputParams(
                user_content=input.name,
                voice=input.voice,
                filename=f"{input.voice.lower().replace(' ', '_')}.mp3"
            ),
            task_queue="lmnt",
            start_to_close_timeout=timedelta(minutes=2)
        )

        return {
            "audiofile_path": audiofile_path
        }


