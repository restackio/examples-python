import os
from restack_ai import Restack
from restack_ai.restack import CloudConnectionOptions
from restack_ai.security import converter
import dataclasses
from .codec import EncryptionCodec

connection_options = CloudConnectionOptions(
    engine_id=os.getenv("RESTACK_ENGINE_ID"),
    api_key=os.getenv("RESTACK_ENGINE_API_KEY"),
    address=os.getenv("RESTACK_ENGINE_ADDRESS"),
    data_converter=dataclasses.replace(converter.default(), payload_codec=EncryptionCodec())
)
client = Restack(connection_options)
