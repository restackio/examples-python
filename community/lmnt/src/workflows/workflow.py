import asyncio
from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow, workflow_info

from .child import ChildWorkflow, ChildWorkflowInput

with import_functions():
    from src.functions.list_voices import lmnt_list_voices


class ExampleWorkflowInput(BaseModel):
    max_amount: int = Field(default=5)


@workflow.defn()
class ExampleWorkflow:
    @workflow.run
    async def run(
        self,
        example_workflow_input: ExampleWorkflowInput,
    ) -> dict[str, list[str]]:
        parent_workflow_id = workflow_info().workflow_id

        voices_response = await workflow.step(
            lmnt_list_voices,
            task_queue="lmnt",
            start_to_close_timeout=timedelta(minutes=2),
        )

        voice_list = voices_response["voices"]
        log.info(
            "Starting to process %s voices",
            min(len(voice_list), example_workflow_input.max_amount),
        )

        tasks = []
        for i, voice in enumerate(voice_list[: example_workflow_input.max_amount]):
            log.info(
                "Creating ChildWorkflow %s for voice %s",
                i + 1,
                voice["name"],
            )
            child_input = ChildWorkflowInput(
                name=f"Hi, my name is {voice['name']}",
                voice=voice["id"],
            )
            task = workflow.child_execute(
                ChildWorkflow,
                workflow_id=f"{parent_workflow_id}-child-execute-{i+1}",
                input=child_input,
            )
            tasks.append(task)
            log.info("Created ChildWorkflow %s", i + 1)

        log.info("Waiting for %s child workflows to complete", len(tasks))
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results, start=1):
            log.info(
                "ChildWorkflow %s completed",
                i,
                audiofile_path=result["audiofile_path"],
            )

        return {
            "results": [result["audiofile_path"] for result in results],
        }
