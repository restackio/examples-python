import aiohttp
from bs4 import BeautifulSoup
from restack_ai.function import FunctionFailure, function, log


@function.defn()
async def crawl_website(url: str) -> str:
    try:
        # Send a GET request to the URL
        async with aiohttp.ClientSession() as session, session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            response.raise_for_status()  # Raise an error for bad responses

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the text content from the page
        content = soup.get_text()
    except Exception as e:
        error_message = "crawl_website function failed"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e
    else:
        log.info("crawl_website", extra={"content": content})
        return content
