from pydantic import BaseModel
from restack_ai.workflow import workflow, import_functions, log
import json

with import_functions():
    from src.functions.get_bot_transcript import get_bot_transcript, GetBotTranscriptInput
    from src.functions.list_bots import list_bots, ListBotsInput
    from src.functions.summarize_transcript import summarize_transcript, SummarizeTranscriptInput
    from src.workflows.create_meet_bot import CreateMeetBotWorkflow
    from src.functions.create_meet_bot import CreateMeetBotInput

class SummarizeMeetingInput(BaseModel):
    meeting_url: str

@workflow.defn()
class SummarizeMeetingWorkflow:
    @workflow.run
    async def run(self, input: SummarizeMeetingInput):
        log.info("SummarizeMeetingWorkflow started")
        bots = await workflow.step(list_bots, ListBotsInput(), task_queue='recall')
        existing_bot = None
        meeting_id = input.meeting_url.split('/')[-1]
        log.info("Meeting ID: ", meeting_id=meeting_id)

        for bot_item in bots["results"]:
            is_done = any(status["code"] == "done" for status in bot_item["status_changes"])
            if meeting_id == bot_item["meeting_url"]["meeting_id"] and is_done:
                existing_bot = bot_item
                break
            
        if existing_bot:
            log.info("Using existing bot")
            transcript = await workflow.step(
                get_bot_transcript,
                GetBotTranscriptInput(bot_id=existing_bot["id"]),
                task_queue='recall'
            )
            transcript_str = json.dumps(transcript)
            summary = await workflow.step(
                summarize_transcript,
                SummarizeTranscriptInput(transcript=transcript_str),
                task_queue='gemini'
            )
            return {
                "bot": existing_bot,
                "transcript": transcript,
                "summary": summary
            }
        else:
            log.info("No existing bot found, create a new bot")
            
            return {
                "message": "No existing bot found, create a new bot",
                "meeting_url": input.meeting_url
            }
