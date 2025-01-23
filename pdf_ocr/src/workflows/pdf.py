from restack_ai.workflow import workflow, import_functions, log
from datetime import timedelta
from pydantic import BaseModel,Field
from typing import List

with import_functions():
    from src.functions.torch_ocr import torch_ocr, OcrInput
    from src.functions.openai_chat import openai_chat, OpenAiChatInput

class PdfWorkflowInput(BaseModel):
    file_upload: List[dict] = Field(files=True)

@workflow.defn()
class PdfWorkflow:
    @workflow.run
    async def run(self, input: PdfWorkflowInput):
        log.info("PdfWorkflow started")

        ocr_result = await workflow.step(
            torch_ocr,
            OcrInput(
                file_type=input.file_upload[0]['type'],
                file_name=input.file_upload[0]['name']
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )

        llm_result = await workflow.step(
            openai_chat,
            OpenAiChatInput(
                user_content=f"Make a summary of that PDF. Here is the OCR result: {ocr_result}",
                model="gpt-4o-mini"
            ),
            start_to_close_timeout=timedelta(seconds=120)
        )

        log.info("PdfWorkflow completed")
        return llm_result
