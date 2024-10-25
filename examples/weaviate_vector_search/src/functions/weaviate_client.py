import os
import weaviate
from weaviate.classes.init import Auth

def get_weaviate_client():
		weaviate_url = os.environ["WEAVIATE_URL"]
		weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

		client = weaviate.connect_to_weaviate_cloud(
				cluster_url=weaviate_url,
				auth_credentials=Auth.api_key(weaviate_api_key),
		)
		return client
