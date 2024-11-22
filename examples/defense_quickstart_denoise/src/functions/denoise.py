from restack_ai.function import function, log
from dataclasses import dataclass
import sieve

@dataclass
class FunctionInputParams:
    file_data: tuple[str, str]

@function.defn()
async def denoise(input: FunctionInputParams):
    try:
        log.info("denoise function started", input=input)

        file_path, _ = input.file_data

        file = sieve.File(path=file_path)
        backend = "aicoustics"
        task = "all"
        enhancement_steps = 64

        audio_enhance = sieve.function.get("sieve/audio-enhance")
        output = audio_enhance.run(file, backend, task, enhancement_steps).path

        log.info("denoise function completed", output=output)
        return output        

    except Exception as e:
        log.error("denoise function failed", error=e)
        raise e
