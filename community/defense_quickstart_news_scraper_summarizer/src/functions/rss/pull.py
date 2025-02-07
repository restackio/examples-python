import xml.etree.ElementTree as ET

import aiohttp
from restack_ai.function import FunctionFailure, function, log

from .schema import RssInput


@function.defn()
async def rss_pull(rss_pull_input: RssInput) -> list[dict]:
    try:
        # Fetch the RSS feed
        async with aiohttp.ClientSession() as session, session.get(
            rss_pull_input.url,
            timeout=aiohttp.ClientTimeout(total=10),
        ) as response:
            response.raise_for_status()  # Raise an error for bad responses

        # Parse the RSS feed
        root = ET.fromstring(response.content)  # noqa: S314
        items = []
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            description = item.find("description").text
            category = (
                item.find("category").text
                if item.find("category") is not None
                else None
            )
            creator = (
                item.find("{http://purl.org/dc/elements/1.1/}creator").text
                if item.find("{http://purl.org/dc/elements/1.1/}creator") is not None
                else None
            )
            pub_date = (
                item.find("pubDate").text if item.find("pubDate") is not None else None
            )
            content_encoded = (
                item.find("{http://purl.org/rss/1.0/modules/content/}encoded").text
                if item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
                is not None
                else None
            )

            items.append(
                {
                    "title": title,
                    "link": link,
                    "description": description,
                    "category": category,
                    "creator": creator,
                    "pub_date": pub_date,
                    "content_encoded": content_encoded,
                },
            )

        # Limit the number of items based on input.count
        max_count = (
            rss_pull_input.count if rss_pull_input.count is not None else len(items)
        )
        items = items[:max_count]
    except Exception as error:
        error_message = "rss_pull function failed"
        log.error(error_message, error=error)
        raise FunctionFailure(error_message, non_retryable=True) from error
    else:
        log.info("rss_pull function succeeded", data=items)
        return items
