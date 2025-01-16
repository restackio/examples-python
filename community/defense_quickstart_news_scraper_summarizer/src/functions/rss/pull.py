import requests
import xml.etree.ElementTree as ET
from restack_ai.function import function, log

from .schema import RssInput

@function.defn()
async def rss_pull(input:RssInput):
    try:
        # Fetch the RSS feed
        response = requests.get(input.url)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the RSS feed
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall(".//item"):
            title = item.find("title").text
            link = item.find("link").text
            description = item.find("description").text
            category = item.find("category").text if item.find("category") is not None else None
            creator = item.find("{http://purl.org/dc/elements/1.1/}creator").text if item.find("{http://purl.org/dc/elements/1.1/}creator") is not None else None
            pub_date = item.find("pubDate").text if item.find("pubDate") is not None else None
            content_encoded = item.find("{http://purl.org/rss/1.0/modules/content/}encoded").text if item.find("{http://purl.org/rss/1.0/modules/content/}encoded") is not None else None

            items.append({
                "title": title,
                "link": link,
                "description": description,
                "category": category,
                "creator": creator,
                "pub_date": pub_date,
                "content_encoded": content_encoded
            })

        # Limit the number of items based on input.count
        max_count = input.count if input.count is not None else len(items)
        items = items[:max_count]

        log.info("rss_pull", extra={"data": items})
        return items
    except Exception as error:
        log.error("rss_pull function failed", error=error)
        raise error