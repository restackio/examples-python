from restack_ai.workflow import workflow, import_functions, log
from dataclasses import dataclass

with import_functions():
    from src.functions.transcribe_audio import transcribe_audio, TranscribeAudioInput
    from src.functions.translate_text import translate_text, TranslateTextInput

@dataclass
class WorkflowInputParams:
    file_path: str
    target_language: str

@workflow.defn()
class TranscribeTranslateWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("TranscribeTranslateWorkflow started", input=input)

        transcription = await workflow.step(
            transcribe_audio,
            TranscribeAudioInput(
                file_path=input.file_path,
            ),
        )

        translation = await workflow.step(
            translate_text,
            TranslateTextInput(
                text=transcription,
                target_language=input.target_language,
            ),
        )

        return {
            "transcription": transcription,
            "translation": translation
        }
