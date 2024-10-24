import json
import weaviate
import requests

from weaviate.classes.init import Auth
from restack_ai.function import function
import weaviate.classes as wvc

from dataclasses import dataclass
@dataclass
class InputParams:
    name: str

@function.defn(name="goodbye")
async def goodbye(input: InputParams) -> str:
    return f"Goodbye, {input.name}!"

@function.defn(name="welcome")
async def welcome(input: InputParams) -> str:
    # import os
    # weaviate_url = os.environ["WEAVIATE_URL"]
    # weaviate_api_key = os.environ["WEAVIATE_API_KEY"]


    # Connect to Weaviate Cloud
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )

    print(client.is_ready())

    # Create the collection. Weaviate's autoschema feature will infer properties when importing.
    if not client.collections.exists("Question"):
        questions = client.collections.create(
            "Question",
            vectorizer_config=wvc.config.Configure.Vectorizer.none(),
        )
    else:
        questions = client.collections.get("Question")

    fname = "jeopardy_tiny_with_vectors_all-OpenAI-ada-002.json"  # This file includes pre-generated vectors
    url = f"https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/{fname}"
    resp = requests.get(url)
    data = json.loads(resp.text)  # Load data

    question_objs = list()
    for i, d in enumerate(data):
        question_objs.append(wvc.data.DataObject(
            properties={
                "answer": d["Answer"],
                "question": d["Question"],
                "category": d["Category"],
            },
            vector=d["vector"]
        ))

    questions = client.collections.get("Question")
    questions.data.insert_many(question_objs)    # This uses batching under the hood




    return f"client.is_ready(), {client.is_ready()}"