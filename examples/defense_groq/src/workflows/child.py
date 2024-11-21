from datetime import timedelta
from dataclasses import dataclass
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.transcribe import transcribe, FunctionInputParams as TranscribeFunctionInputParams
    from src.functions.translate import translate, FunctionInputParams as TranslationFunctionInputParams
    from src.functions.fix_sentence import fix_sentence, FunctionInputParams as FixSentenceFunctionInputParams
@dataclass
class WorkflowInputParams:
    file_data: tuple[str, str]

@dataclass
class WorkflowOutputParams:
    transcription: str
    fixed_sentence: str
    translation: str

@workflow.defn()
class ChildWorkflow:
    @workflow.run
    async def run(self, input: WorkflowInputParams):
        log.info("TranscribeWorkflow started", input=input)

        transcription = await workflow.step(
            transcribe,
            TranscribeFunctionInputParams(file_data=input.file_data),
            start_to_close_timeout=timedelta(seconds=120)
        )

        fix_sentence_prompt = f"""
        Instructions: Fix the following content to make it grammatically correct and make sense.
        Content: {transcription['text']}
        """

        fixed_sentence = await workflow.step(
            fix_sentence,
            FixSentenceFunctionInputParams(user_prompt=fix_sentence_prompt),
            start_to_close_timeout=timedelta(seconds=120)
        )

        translation_prompt = f"""
        Instructions: Translate the following content to English.
        Content: {fixed_sentence['content']}
        """

        translation = await workflow.step(
            translate,
            TranslationFunctionInputParams(user_prompt=translation_prompt),
            start_to_close_timeout=timedelta(seconds=120)
        )

        log.info("ChildWorkflow completed", transcription=transcription['text'], fixed_sentence=fixed_sentence['content'], translation=translation['content'])
        return WorkflowOutputParams(
            transcription=transcription['text'],
            fixed_sentence=fixed_sentence['content'],
            translation=translation['content']
        )
