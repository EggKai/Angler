from pathlib import Path
from typing import List, Set
import cv2
import numpy as np
from pyzbar.pyzbar import decode #if u see an import error; check https://www.microsoft.com/en-US/download/details.aspx?id=40784

def read_qr_codes(image_path: str) -> List[str]:
        """
        Reads multiple QR codes from a given image file.

        Args:
            image_path (Path): The path to the image file.

        Returns:
            List[str]: A sorted list of unique decoded QR code data. 
                       Returns an empty list if no QR codes are found.

        Raises:
            FileNotFoundError: If the image file does not exist.
            ValueError: If the image cannot be loaded.
        """
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")

        img = cv2.imread(image_path) # Load the image
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")

        # Convert to grayscale for better QR detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect and decode QR codes
        decoded_objects = decode(gray)

        # Extract QR code data, remove duplicates, and sort results
        qr_results: Set[str] = {obj.data.decode("utf-8") for obj in decoded_objects}

        return sorted(qr_results)  # Sorting ensures consistent order of results

if __name__ == "__main__":
    # Example Usage
    image_path = "qr_code.png"  # Replace with your image path
    qr_data = read_qr_codes(image_path)
    print("QR Code Data:", qr_data if qr_data else "No QR code found.")
