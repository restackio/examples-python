from datetime import timedelta
from dataclasses import dataclass
from restack_ai.workflow import workflow, import_functions, log

@dataclass
class WorkflowInputParams:
    file_data: tuple[str, str]


@dataclass
class WorkflowOutputParams:
    cleaned_audio: str


@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams) -> WorkflowOutputParams:
        log.info("ChildWorkflow started", input=input)
        return WorkflowOutputParams(cleaned_audio="cleaned_audio")