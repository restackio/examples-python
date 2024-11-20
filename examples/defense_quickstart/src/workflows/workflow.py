from datetime import timedelta
from restack_ai.workflow import workflow, import_functions, log

with import_functions():
    from src.functions.rss.pull import rss_pull
    from src.functions.crawl.website import crawl_website
    from src.functions.llm.chat import llm_chat, FunctionInputParams
    from src.functions.rss.schema import RssInput

@workflow.defn()
class RssWorkflow:
    @workflow.run
    async def run(self, input: dict):

        url = input["url"]
        count = input["count"]
        rss_results = await workflow.step(rss_pull, RssInput(url=url, count=count), start_to_close_timeout=timedelta(seconds=10))
        urls = [item['link'] for item in rss_results if 'link' in item]

        crawled_contents = []
        for url in urls:  # Use the extracted URLs
            log.info("rss_result", extra={"url": url})
            if url:
                content = await workflow.step(crawl_website, url, start_to_close_timeout=timedelta(seconds=30))
                
                crawled_contents.append(content)
        
        summaries = []
        for content in crawled_contents:
            user_prompt = f"Provide a translation of the news article. Translate the following content: {content}"
            translation = await workflow.step(llm_chat, FunctionInputParams(user_prompt=user_prompt), task_queue="llm_chat",start_to_close_timeout=timedelta(seconds=120))

            user_prompt = f"Provide a summary of the news found on rss feed. Summarize the following content: {translation}"
            summary = await workflow.step(llm_chat, FunctionInputParams(user_prompt=user_prompt), task_queue="llm_chat",start_to_close_timeout=timedelta(seconds=120))
            summaries.append(summary)

        user_prompt = f"You are a personal assistant. Provide a summary of the latest news and the summaries of the websites. Structure your response with the title of the project, then a short description and a list of actionable bullet points. Here is the latest rss data: {str(rss_results)} and summaries of the websites: {str(summaries)}"

        return await workflow.step(llm_chat, FunctionInputParams(user_prompt=user_prompt), task_queue="llm_chat", start_to_close_timeout=timedelta(seconds=120))