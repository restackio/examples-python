from datetime import timedelta
from dataclasses import dataclass
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.denoise import denoise, FunctionInputParams as DenoiseFunctionInputParams

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

        cleaned_audio = await workflow.step(
            denoise,
            DenoiseFunctionInputParams(file_data=input.file_data),
            start_to_close_timeout=timedelta(seconds=120)
        )

        log.info("ChildWorkflow completed", cleaned_audio=cleaned_audio)
        return WorkflowOutputParams(cleaned_audio=cleaned_audio)