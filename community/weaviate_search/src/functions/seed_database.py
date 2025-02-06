import json

import aiohttp
import weaviate.classes as wvc
from restack_ai.function import function, log

from src.functions.weaviate_client import get_weaviate_client


@function.defn()
async def seed_database() -> str:
    client = get_weaviate_client()

    try:
        # Create the collection.
        # Weaviate's autoschema feature will infer properties when importing.
        if not client.collections.exists("Question"):
            questions = client.collections.create(
                "Question",
                vectorizer_config=wvc.config.Configure.Vectorizer.none(),
            )
        else:
            questions = client.collections.get("Question")

        # This file includes pre-generated vectors
        fname = "jeopardy_tiny_with_vectors_all-OpenAI-ada-002.json"

        url = f"https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/{fname}"
        async with aiohttp.ClientSession() as session, session.get(
                url, timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
            response.raise_for_status()  # Raise an error for bad responses
            data = json.loads(await response.text())  # Load data

        question_objs = []
        for _i, d in enumerate(data):
            question_objs.append(
                wvc.data.DataObject(
                    properties={
                        "answer": d["Answer"],
                        "question": d["Question"],
                        "category": d["Category"],
                    },
                    vector=d["vector"],
                ),
            )

        questions = client.collections.get("Question")
        questions.data.insert_many(question_objs)  # This uses batching under the hood

        log.info("seed_database function completed")

        return "Data has been seeded"
    finally:
        client.close()
