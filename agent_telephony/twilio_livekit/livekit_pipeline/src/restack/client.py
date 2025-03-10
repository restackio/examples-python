"""Client.

Initializes and exposes the Restack client used for sending events from the LiveKit pipeline agent.
"""

import os

from dotenv import load_dotenv
from restack_ai import Restack
from restack_ai.restack import CloudConnectionOptions
from src.utils import logger

# Load environment variables from the .env file.
load_dotenv()

try:
    engine_id = os.getenv("RESTACK_ENGINE_ID")
    address = os.getenv("RESTACK_ENGINE_ADDRESS")
    api_key = os.getenv("RESTACK_ENGINE_API_KEY")
    api_address = os.getenv("RESTACK_ENGINE_API_ADDRESS")

    connection_options = CloudConnectionOptions(
        engine_id=engine_id,
        address=address,
        api_key=api_key,
        api_address=api_address,
    )
    client = Restack(connection_options)
    logger.info(
        "Initialized Restack client with engine_id: %s", engine_id
    )
except Exception as e:
    logger.exception("Error initializing Restack client: %s", e)
    raise
