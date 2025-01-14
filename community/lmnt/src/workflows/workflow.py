import asyncio
from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, log, workflow_info, import_functions
from .child import ChildWorkflow, ChildWorkflowInput

with import_functions():
    from src.functions.list_voices import lmnt_list_voices


class ExampleWorkflowInput(BaseModel):
    max_amount: int = Field(default=5)

@workflow.defn()
class ExampleWorkflow:
    @workflow.run
    async def run(self, input: ExampleWorkflowInput):
        parent_workflow_id = workflow_info().workflow_id
        
        voices_response = await workflow.step(
            lmnt_list_voices,
            task_queue="lmnt",
            start_to_close_timeout=timedelta(minutes=2)
        )
        
        voice_list = voices_response["voices"]
        log.info(f"Starting to process {min(len(voice_list), input.max_amount)} voices")

        tasks = []
        for i, voice in enumerate(voice_list[:input.max_amount]):
            log.info(f"Creating ChildWorkflow {i+1} for voice {voice['name']}")
            child_input = ChildWorkflowInput(
                name=f"Hi, my name is {voice['name']}", 
                voice=voice['id']
            )
            task = workflow.child_execute(
                ChildWorkflow, 
                workflow_id=f"{parent_workflow_id}-child-execute-{i+1}",
                input=child_input
            )
            tasks.append(task)
            log.info(f"Created ChildWorkflow {i+1}")

        log.info(f"Waiting for {len(tasks)} child workflows to complete")
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results, start=1):
            log.info(f"ChildWorkflow {i} completed", audiofile_path=result['audiofile_path'])

        return {
            "results": [result['audiofile_path'] for result in results]
        }