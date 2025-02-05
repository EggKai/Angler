import requests
import tempfile
import os
import warnings
from typing import List, Union, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from OCR import process_images
from QRdetection import read_qr_codes
def get_image_extension_from_response(response: requests.Response) -> str:
    """Determine the image file extension based on content type."""
    content_type: str = response.headers.get('Content-Type', '')
    if 'image/png' in content_type:
        return '.png'
    elif 'image/jpeg' in content_type:
        return '.jpg'
    return '.jpg'  # Default to .jpg if unknown format

class DownloadFile:
    """Context manager for handling single or multiple temporary file downloads using multithreading."""

    def __init__(self, url_or_urls: Union[str, List[str]]):
        """Initialize with a single URL or a list of URLs."""
        self.urls = [url_or_urls] if isinstance(url_or_urls, str) else url_or_urls
        self.temp_file_paths: List[str] = []

    def _download_image(self, url: str) -> Optional[str]:
        """Download a single image and return its temporary file path."""
        try:
            response = requests.get(url, timeout=10)  # Timeout to prevent hanging
            if response.status_code == 200:
                file_extension = get_image_extension_from_response(response)
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    temp_file.write(response.content)
                    return temp_file.name
            else:
                warnings.warn(f"Error: Failed to download image from {url} (Status: {response.status_code})")
        except Exception as e:
            warnings.warn(f"Error downloading {url}: {e}")
        return None

    def __enter__(self) -> Optional[List[str]]:
        """Download the file(s) using multithreading and return their temporary paths."""
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(self._download_image, url): url for url in self.urls}
            for future in as_completed(future_to_url):
                temp_path = future.result()
                if temp_path:
                    self.temp_file_paths.append(temp_path)
        return self.temp_file_paths if self.temp_file_paths else None

    def __exit__(self, exc_type, exc_value, traceback):
        """Ensure all temporary files are deleted after exiting the context."""
        for temp_path in self.temp_file_paths:
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    # Run the function
    image_urls:List[str] = [
    "https://global-uploads.webflow.com/5e5ff4f0165cd367cc7ca88f/6009e9edba9c2ab78a6245d7_PayPal-01.png",
    "https://cdn.freewebstore.com/origin/194139/honestynelvp12p49_1676741562675.jpg",
    "https://ci3.googleusercontent.com/meips/ADKq_NaDBZgPu-UBOGDfTfx7Sx_yWSv9jeXK-AUJM_J3cffNJDvLV2SnUtqsm0XERTpb-pOrXCZNCSGPnIFX3GtFwZe_J39LebJaJUOYjC9yMn0dk55tbNTXyhQcQabHYE0=s0-d-e1-ft#https://store.fastly.steamstatic.com/public/shared/images/email/logo.png",
    "https://ci3.googleusercontent.com/meips/ADKq_NZJIC2JBSjMhze-MBGXwWVKf6F8HrWgsvceSVQ6yI_BzV8NXA0QEpjX8phgXKPRS2UV_ZqM9sPxZvxvfjO7FsQ9-nd0sgPpe-cZUkq9af3MmTkUszKVM41E2G8Lq1eFE5OfDbiP=s0-d-e1-ft#https://store.fastly.steamstatic.com/public/shared/images/email/logo_footer.png",
    "https://ci3.googleusercontent.com/meips/ADKq_NYPXiiD1xdxO-VuDkoefXKFCriPR-L50EZ456kU3UmuH6uFLuGb8g-lELUSRmCsBqrmCedFK-m3jGVh8qnDNo1I97N2nbSyT06Xc41Y1hJydfHdZTLbrDn7-EH2ktKYzoxB-w4=s0-d-e1-ft#https://store.fastly.steamstatic.com/public/shared/images/email/logo_valve.jpg",
    "https://ci3.googleusercontent.com/meips/ADKq_NYcUVoMGWTs6tbLLNcP55TKkIZMN5ydD63F1BRr3mAU3yktur9Efp_Fh0eNLIRfoj8zS29TeFnknurb2nlibE_gkeAeLuHi3XQpx9NDL746o4OUzCFn=s0-d-e1-ft#https://cdn.fastly.steamstatic.com/store/email/general/ico_x.png"
    ]
    with DownloadFile(image_urls) as temp_files:
        print(dict(zip(image_urls, process_images(temp_files)))) #not using ziplongest as we are not expecting it to fail

    image_QRs:List[str] = [
        "https://i.pinimg.com/originals/b7/24/8c/b7248c7d3b8b9d5990b9174d22e43d0f.png"
    ]
    with DownloadFile(image_QRs) as temp_files:
        for file in temp_files:
            qr_data = read_qr_codes(file)
            print("QR Code Data:", qr_data if qr_data else "No QR code found.")