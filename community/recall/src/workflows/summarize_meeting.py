from datetime import timedelta
from pydantic import BaseModel, Field
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.create_meet_bot import create_meet_bot, CreateMeetBotInput
    from src.functions.get_bot_transcript import get_bot_transcript, GetBotTranscriptInput
    from src.functions.list_bots import list_bots, ListBotsInput
class SummarizeMeetingInput(BaseModel):
    meeting_url: str

@workflow.defn()
class SummarizeMeetingWorkflow:
    @workflow.run
    async def run(self, input: SummarizeMeetingInput):
        log.info("SummarizeMeetingWorkflow started")
        # Get list of existing bots
        bots = await workflow.step(list_bots, ListBotsInput())
        
        # Check if there's already a bot for this meeting URL
        existing_bot = None
        for bot in bots["results"]:
            if bot["meeting_url"] == input.meeting_url:
                existing_bot = bot
                break
                
        if existing_bot:
            bot = existing_bot
            log.info("Using existing bot")
        else:
            # Create new bot if none exists
            log.info("Creating new bot")
            # bot = await workflow.step(create_meet_bot, CreateMeetBotInput(meeting_url=input.meeting_url))
        
        # created_bot = await workflow.step(create_meet_bot, CreateMeetBotInput(meeting_url=input.meeting_url))
        # retrieved_bot = await workflow.step(retrieve_bot, RetrieveBotInput(bot_id=created_bot["id"]))
        
        transcript = await workflow.step(get_bot_transcript, GetBotTranscriptInput(bot_id=bot["id"]))
        
        return {
            "bot": bot,
            "transcript": transcript
        }


