"""Client module for LMNT API integration."""
import os
from lmnt.api import Speech
from dotenv import load_dotenv

load_dotenv()

async def lmnt_client() -> Speech:
    """Initialize and return LMNT Speech client.
    
    Raises:
        ValueError: If LMNT_API_KEY environment variable is not set
        RuntimeError: If client initialization fails
    """
    api_key = os.getenv('LMNT_API_KEY')
    if not api_key:
        raise ValueError("LMNT_API_KEY environment variable is not set")
    try:
        return Speech(api_key)
    except Exception as e:
        raise RuntimeError(f"Failed to initialize LMNT client: {str(e)}") from e
