import os
from restack_ai import Restack
from restack_ai.restack import CloudConnectionOptions
from dotenv import load_dotenv  

from src.functions.smtp_send_email import load_smtp_config
# Load environment variables from a .env file
load_dotenv()

# Call and validate environment variables for critical functions - prevents app from running if we don't have the necessary environment variables
# Possible standard practice for all functions that require environment variables? 
# Most examples have long blocks of checking for environment variables, so this could be a good way to consolidate that to a standard function we 
# can short circuit and kill the app if we know we will have a failure state.

## Verify ENV VARS present for SMTP Send Email function
load_smtp_config()

engine_id = os.getenv("RESTACK_ENGINE_ID")
address = os.getenv("RESTACK_ENGINE_ADDRESS")
api_key = os.getenv("RESTACK_ENGINE_API_KEY")

connection_options = CloudConnectionOptions(
    engine_id=engine_id,
    address=address,
    api_key=api_key
)
client = Restack(connection_options)


# 