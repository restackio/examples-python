from datetime import timedelta

from pydantic import BaseModel
from restack_ai.workflow import RetryPolicy, import_functions, log, workflow

with import_functions():
    from src.functions.multi_function_call_advanced import (
        ChatMessage,
        FunctionInputParams,
        gemini_multi_function_call_advanced,
    )


class MultiFunctionCallAdvancedInputParams(BaseModel):
    user_content: str = "What's the weather in San Francisco?"


@workflow.defn()
class GeminiMultiFunctionCallAdvancedWorkflow:
    def __init__(self):
        self.chat_history = []

    @workflow.run
    async def run(self, input: MultiFunctionCallAdvancedInputParams):
        log.info("GeminiMultiFunctionCallAdvancedWorkflow started", input=input)

        current_content = input.user_content
        final_response = None
        function_results = []

        while True:
            result = await workflow.step(
                gemini_multi_function_call_advanced,
                FunctionInputParams(
                    user_content=current_content,
                    chat_history=self.chat_history,
                ),
                schedule_to_close_timeout=timedelta(seconds=860),
                start_to_close_timeout=timedelta(seconds=860),
                retry_policy=RetryPolicy(maximum_attempts=3),
                task_queue="gemini",
            )

            if not result or not isinstance(result, dict):
                break

            has_function_calls = False

            for candidate in result.get("candidates", []):
                for part in candidate.get("content", {}).get("parts", []):
                    if part.get("text"):
                        final_response = part["text"]
                    elif part.get("functionCall"):
                        has_function_calls = True
                        func_call = part["functionCall"]
                        function_name = func_call["name"]

                        if function_name in {
                            "get_current_temperature",
                            "get_humidity",
                            "get_air_quality",
                        }:
                            try:
                                result = await workflow.step(
                                    globals()[function_name],
                                    func_call["args"],
                                    task_queue="tools",
                                    retry_policy=RetryPolicy(maximum_attempts=1),
                                )
                                function_results.append(
                                    f"{function_name} result: {result!s}",
                                )
                                log.info(
                                    f"Function {function_name} executed successfully",
                                    result=result,
                                )
                            except Exception as e:
                                function_results.append(
                                    f"Error executing {function_name}: {e!s}",
                                )
                                log.error(f"Error executing {function_name}: {e!s}")

            if not has_function_calls:
                break

            if function_results:
                current_content = f"Based on these results: {'; '.join(function_results)}, please provide a final answer."
                self.chat_history.append(
                    ChatMessage(role="user", content=current_content),
                )
                function_results = []
            else:
                break

        return {
            "response": final_response,
        }
