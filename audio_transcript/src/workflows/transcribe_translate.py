from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.transcribe_audio import TranscribeAudioInput, transcribe_audio
    from src.functions.translate_text import TranslateTextInput, translate_text

class WorkflowInputParams(BaseModel):
    file_path: str = Field(default="/test.mp3")
    target_language: str = Field(default="fr")

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
            "translation": translation,
        }
