from dataclasses import dataclass
from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.transcribe import (
        FunctionInputParams as TranscribeFunctionInputParams,
    )
    from src.functions.transcribe import transcribe
    from src.functions.translate import (
        FunctionInputParams as TranslationFunctionInputParams,
    )
    from src.functions.translate import translate

@dataclass
class WorkflowInputParams:
    file_data: tuple[str, str]

@dataclass
class WorkflowOutputParams:
    transcription: str
    translation: str

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("ChildWorkflow started", input=input)

        transcription = await workflow.step(
            transcribe,
            TranscribeFunctionInputParams(file_data=input.file_data),
            start_to_close_timeout=timedelta(seconds=120),
        )

        translation_prompt = f"""
        Instructions: Translate the following content to English. Output only the translated content.
        Content: {transcription['text']}
        """

        translation = await workflow.step(
            translate,
            TranslationFunctionInputParams(user_prompt=translation_prompt),
            start_to_close_timeout=timedelta(seconds=120),
        )

        log.info("ChildWorkflow completed", transcription=transcription["text"], translation=translation["content"])
        return WorkflowOutputParams(
            transcription=transcription["text"],
            translation=translation["content"],
        )
