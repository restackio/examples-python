from restack_ai.function import function, log
from dataclasses import dataclass
import sieve
import os

@dataclass
class FunctionInputParams:
    file_data: tuple[str, str]

@function.defn()
async def remove_noise(input: FunctionInputParams):
    try:
        log.info("remove_noise function started", input=input)

        file = sieve.File(path=input.file_data[0])
        backend = "aicoustics"
        task = "all"
        enhancement_steps = 64

        audio_enhance = sieve.function.get("sieve/audio-enhance")
        output = audio_enhance.run(file, backend, task, enhancement_steps)

        log.info("remove_noise function completed", output=output)
        return output        

    except Exception as e:
        log.error("remove_noise function failed", error=e)
        raise e
