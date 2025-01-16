from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.create_meet_bot import create_meet_bot, CreateMeetBotInput

@workflow.defn()
class CreateMeetBotWorkflow:
    @workflow.run
    async def run(self, input: CreateMeetBotInput):
        log.info("CreateMeetBotWorkflow started")
        bot = await workflow.step(create_meet_bot, input, task_queue='recall')
        return bot