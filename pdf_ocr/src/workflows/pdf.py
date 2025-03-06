from datetime import timedelta

from pydantic import BaseModel, Field
from restack_ai.workflow import NonRetryableError, import_functions, log, workflow

with import_functions():
    from src.functions.openai_chat import OpenAiChatInput, openai_chat
    from src.functions.torch_ocr import OcrInput, torch_ocr

class PdfWorkflowInput(BaseModel):
    file_upload: list[dict] = Field(files=True)

@workflow.defn()
class PdfWorkflow:
    @workflow.run
    async def run(self, input: PdfWorkflowInput):
        log.info("PdfWorkflow started")
        try:
            ocr_result = await workflow.step(
                function=torch_ocr,
                function_input=OcrInput(
                    file_type=input.file_upload[0]["type"],
                    file_name=input.file_upload[0]["name"]
                ),
                start_to_close_timeout=timedelta(seconds=120)
            )
        except Exception as e:
            error_message = f"torch_ocr function failed: {e}"
            raise NonRetryableError(error_message) from e
        else:

            try:
                llm_result = await workflow.step(
                    function=openai_chat,
                    function_input=OpenAiChatInput(
                        user_content=f"Make a summary of that PDF. Here is the OCR result: {ocr_result}",
                        model="gpt-4o-mini"
                    ),
                    start_to_close_timeout=timedelta(seconds=120)
                )
            except Exception as e:
                error_message = f"openai_chat function failed: {e}"
                raise NonRetryableError(error_message) from e
            else:
                log.info("PdfWorkflow completed")
                return llm_result
