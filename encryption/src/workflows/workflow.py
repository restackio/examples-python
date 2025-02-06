from datetime import timedelta

from restack_ai.workflow import import_functions, log, workflow

with import_functions():
    from src.functions.function import welcome


@workflow.defn()
class EncryptedWorkflow:
    @workflow.run
    async def run(self) -> str:
        log.info("EncryptedWorkflow started")
        result = await workflow.step(
            welcome,
            input="world",
            start_to_close_timeout=timedelta(seconds=120),
        )
        log.info("EncryptedWorkflow completed", result=result)
        return result
