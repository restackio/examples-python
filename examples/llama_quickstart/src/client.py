import os
from restack_ai import Restack
from restack_ai.restack import CloudConnectionOptions
from dotenv import load_dotenv  

# Load environment variables from a .env file
load_dotenv()


engine_id = os.getenv("RESTACK_ENGINE_ID")
address = os.getenv("RESTACK_ENGINE_ADDRESS")
api_key = os.getenv("RESTACK_ENGINE_API_KEY")

connection_options = CloudConnectionOptions(
    engine_id=engine_id,
    address=address,
    api_key=api_key
)

client = Restack(connection_options)
