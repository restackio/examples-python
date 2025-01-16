from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log
with import_functions():
    from src.functions.bostondynamics.commands import spot_commands

@workflow.defn()
class SpotWorkflow:
    @workflow.run
    async def run(self):
        log.info("SpotWorkflow started")
        result = await workflow.step(spot_commands, start_to_close_timeout=timedelta(seconds=120))
        log.info("SpotWorkflow completed", result=result)
        return result


