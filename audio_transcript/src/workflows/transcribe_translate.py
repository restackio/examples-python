from restack_ai.workflow import workflow, import_functions, log
from pydantic import BaseModel, Field
with import_functions():
    from src.functions.transcribe_audio import transcribe_audio, TranscribeAudioInput
    from src.functions.translate_text import translate_text, TranslateTextInput

class WorkflowInputParams(BaseModel):
    file_path: str = Field(default="/test.mp3")
    target_language: str = Field(default="fr")

@workflow.defn()
class TranscribeTranslateWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("TranscribeTranslateWorkflow started", input=input)

        transcription = await workflow.step(
            function=transcribe_audio,
            function_input=TranscribeAudioInput(
                file_path=input.file_path,
            ),
        )

        translation = await workflow.step(
            function=translate_text,
            function_input=TranslateTextInput(
                text=transcription,
                target_language=input.target_language,
            ),
        )

        return {
            "transcription": transcription,
            "translation": translation
        }
