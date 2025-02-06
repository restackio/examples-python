from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.openai_chat import OpenAiChatInput, openai_chat
    from src.functions.torch_ocr import OcrInput, torch_ocr


class PdfWorkflowInput(BaseModel):
    file_upload: list[dict] = Field(files=True)


@workflow.defn()
class PdfWorkflow:
    @workflow.run
    async def run(self, pdf_workflow_input: PdfWorkflowInput) -> str:
        log.info("PdfWorkflow started")

        ocr_result = await workflow.step(
            torch_ocr,
            OcrInput(
                file_type=pdf_workflow_input.file_upload[0]["type"],
                file_name=pdf_workflow_input.file_upload[0]["name"],
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )

        llm_result = await workflow.step(
            openai_chat,
            OpenAiChatInput(
                user_content=f"""
                Make a summary of that PDF.
                Here is the OCR result:
                {ocr_result}
                """,
                model="gpt-4o-mini",
            ),
            start_to_close_timeout=timedelta(seconds=120),
        )

        log.info("PdfWorkflow completed")
        return llm_result
