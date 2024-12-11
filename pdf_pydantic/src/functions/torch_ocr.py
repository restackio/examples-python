import base64
import io
from typing import Any, List

import numpy as np
from doctr.io import DocumentFile
from fastapi import UploadFile
from numpy.typing import NDArray
from PIL import Image
from pydantic import BaseModel, Field
from restack_ai.function import function
from doctr.models import ocr_predictor

class OCRPrediction(BaseModel):
    pages: List[dict[str, Any]] = Field(
        description="List of pages with OCR predictions"
    )

class OcrInput(BaseModel):
    file_type: str
    file_binary:str

@function.defn()
async def torch_ocr(input: OcrInput) -> str:
    try:
        service = DocumentExtractionService()
        content = base64.b64decode(input.file_binary)

        if input.file_type == "application/pdf":
            doc = DocumentFile.from_pdf(content)
        elif input.file_type.startswith("image/"):
            image: Image.Image = Image.open(io.BytesIO(content))
            processed_img: NDArray[np.uint8] = service._preprocess_image(image)
            doc = DocumentFile.from_images(processed_img)
        else:
            raise ValueError("Unsupported file type")

        result = service.predictor(doc)
        json_output = OCRPrediction.model_validate(result.export())
        return service._process_predictions(json_output)

    except Exception as e:
        raise ValueError(f"Failed to process file: {str(e)}")

class DocumentExtractionService:
    def __init__(self) -> None:
        self.predictor = ocr_predictor(
            det_arch="db_resnet50",
            reco_arch="crnn_vgg16_bn",
            pretrained=True,
            assume_straight_pages=False,
        )

    async def extract(self, file: UploadFile) -> str:
        try:
            content: bytes = await file.read()

            if file.content_type is None:
                raise ValueError("File content type is not available")

            if file.content_type == "application/pdf":
                doc = DocumentFile.from_pdf(content)
            elif file.content_type.startswith("image/"):
                image: Image.Image = Image.open(io.BytesIO(content))
                processed_img: NDArray[np.uint8] = self._preprocess_image(image)
                doc = DocumentFile.from_images(processed_img)
            else:
                raise ValueError("Unsupported file type")

            result = self.predictor(doc)
            json_output = OCRPrediction.model_validate(result.export())
            return self._process_predictions(json_output)

        except Exception as e:
            raise ValueError(f"Failed to process file: {str(e)}")

    def _preprocess_image(self, image: Image.Image) -> NDArray[np.uint8]:
        if image.mode != "RGB":
            image = image.convert("RGB")

        img_array: NDArray[np.uint8] = np.array(image)
        p2, p98 = np.percentile(img_array, (2, 98))
        img_array = np.clip(img_array, p2, p98)
        img_array = ((img_array - p2) / (p98 - p2) * 255).astype(np.uint8)

        return img_array

    def _process_predictions(
        self, json_output: OCRPrediction, confidence_threshold: float = 0.3
    ) -> str:
        processed_text: List[str] = []

        for page in json_output.pages:
            page_text: List[str] = []
            for block in page["blocks"]:
                for line in block["lines"]:
                    line_text: List[str] = []
                    for word in line["words"]:
                        if word["confidence"] > confidence_threshold:
                            line_text.append(word["value"])
                    if line_text:
                        page_text.append(" ".join(line_text))
            processed_text.append("\n".join(page_text))

        return "\n\n=== PAGE BREAK ===\n\n".join(processed_text)