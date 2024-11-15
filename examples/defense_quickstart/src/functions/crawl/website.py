from restack_ai.function import function, log
import requests
from bs4 import BeautifulSoup

@function.defn()
async def crawl_website(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the text content from the page
        content = soup.get_text()

        log.info("crawl_website", extra={"content": content})

        return content

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        log.error("crawl_website function failed", error=e)
        raise e
