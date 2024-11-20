from datetime import timedelta
from dataclasses import dataclass
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.transcribe import transcribe, FunctionInputParams

@dataclass
class WorkflowInputParams:
    file_data: tuple[str, str]

@workflow.defn()
class TranscribeWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("TranscribeWorkflow started", input=input)

        transcription = await workflow.step(
            transcribe,
            FunctionInputParams(file_data=input.file_data),
            start_to_close_timeout=timedelta(seconds=120)
        )

        log.info("TranscribeWorkflow completed", transcription=transcription)
        return transcription
