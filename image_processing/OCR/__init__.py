
import pytesseract
import os
import warnings
from typing import Optional, Set, List, Iterator
from PIL import Image
from .processing import process_image_for_ocr

def perform_ocr(image_path: str) -> Optional[str]:
    """Perform OCR on the given image and return extracted text."""
    preprocessed_image = process_image_for_ocr(image_path)
    if preprocessed_image is None:
        return None
    pil_img: Image.Image = Image.fromarray(preprocessed_image)
    return pytesseract.image_to_string(pil_img, config='--psm 6')

def process_images(file_paths: List[str]) -> Iterator[Set[str]]:
    """Process a list of image file paths for OCR and yield results."""
    for file_path in file_paths:
        if os.path.exists(file_path):
            text: Optional[str] = perform_ocr(file_path)
            if text:#if text exists
                yield text
        else:
            warnings.warn(f"Error: File not found - {file_path}")

