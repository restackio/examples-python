import io
from typing import Any

import aiohttp
import numpy as np
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from numpy.typing import NDArray
from PIL import Image
from pydantic import BaseModel, Field
from restack_ai.function import FunctionFailure, function, log

from src.client import api_address


class OCRPrediction(BaseModel):
    pages: list[dict[str, Any]] = Field(
        description="List of pages with OCR predictions",
    )


class OcrInput(BaseModel):
    file_type: str
    file_name: str


def raise_unsupported_file_type_error() -> None:
    error_message = "Unsupported file type"
    log.error(error_message)
    raise FunctionFailure(error_message, non_retryable=True)


@function.defn()
async def torch_ocr(ocr_input: OcrInput) -> str:
    try:
        service = DocumentExtractionService()

        # Download the file from localhost
        async with aiohttp.ClientSession() as session, session.get(
                f"{api_address or 'http://localhost:6233'}/api/download/{ocr_input.file_name}",
                timeout=aiohttp.ClientTimeout(total=10),
            ) as response:
                response.raise_for_status()  # Raise an error for bad responses
                content = await response.content.read()

        if ocr_input.file_type == "application/pdf":
            doc = DocumentFile.from_pdf(content)
        elif ocr_input.file_type.startswith("image/"):
            image: Image.Image = Image.open(io.BytesIO(content))
            processed_img: NDArray[np.uint8] = service.preprocess_image(image)
            doc = DocumentFile.from_images(processed_img)
        else:
            raise_unsupported_file_type_error()

        result = service.predictor(doc)
        json_output = OCRPrediction.model_validate(result.export())
        return service.process_predictions(json_output)
    except Exception as e:
        error_message = "Failed to process file"
        log.error(error_message, error=e)
        raise FunctionFailure(error_message, non_retryable=True) from e


class DocumentExtractionService:
    def __init__(self) -> None:
        self.predictor = ocr_predictor(
            det_arch="db_resnet50",
            reco_arch="crnn_vgg16_bn",
            pretrained=True,
            assume_straight_pages=False,
        )

    def preprocess_image(self, image: Image.Image) -> NDArray[np.uint8]:
        if image.mode != "RGB":
            image = image.convert("RGB")

        img_array: NDArray[np.uint8] = np.array(image)
        p2, p98 = np.percentile(img_array, (2, 98))
        img_array = np.clip(img_array, p2, p98)
        img_array = ((img_array - p2) / (p98 - p2) * 255).astype(np.uint8)
        log.info("Preprocessed image", img_array=img_array)

        return img_array

    def process_predictions(
        self,
        json_output: OCRPrediction,
        confidence_threshold: float = 0.3,
    ) -> str:
        processed_text: list[str] = []

        for page in json_output.pages:
            page_text = [
                " ".join([
                    word["value"]
                    for word in line["words"]
                    if word["confidence"] > confidence_threshold
                ])
                for block in page["blocks"]
                for line in block["lines"]
                if any(
                    word["confidence"] > confidence_threshold
                    for word in line["words"]
                )
            ]
            processed_text.append("\n".join(page_text))

        return "\n\n=== PAGE BREAK ===\n\n".join(processed_text)
