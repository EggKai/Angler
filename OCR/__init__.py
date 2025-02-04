import requests
import tempfile
import pytesseract
import os
from PIL import Image
import warnings
from processing import process_image_for_ocr
def get_image_extension_from_response(response):
    content_type = response.headers.get('Content-Type', '')
    if 'image/png' in content_type:
        return '.png'
    elif 'image/jpeg' in content_type:
        return '.jpg'
    return '.jpg'  # Default to .jpg if unknown format
def process_images(image_urls):
    for url in image_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                file_extension = get_image_extension_from_response(response) # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file: # Create a temporary file with the correct extension
                    temp_file.write(response.content)
                    temp_file_path = temp_file.name
                preprocessed_image = process_image_for_ocr(temp_file_path) # Preprocess 
                if preprocessed_image is None:
                    warnings.warn(f"Skipping {url} due to preprocessing error.")
                    continue
                pil_img = Image.fromarray(preprocessed_image) # Convert the preprocessed image to PIL format for Tesseract
                text = pytesseract.image_to_string(pil_img, config='--psm 6') # Use Tesseract to extract text (psm6 seems to work the best)
                os.remove(temp_file_path) # Delete the temporary file after processing
                yield {url, text}
            else:
                print(f"Error: Failed to download image from {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

if __name__ == "__main__":
    # Run the function
    image_urls = [
    "https://global-uploads.webflow.com/5e5ff4f0165cd367cc7ca88f/6009e9edba9c2ab78a6245d7_PayPal-01.png",
    "https://cdn.freewebstore.com/origin/194139/honestynelvp12p49_1676741562675.jpg",
    "https://ci3.googleusercontent.com/meips/ADKq_NaDBZgPu-UBOGDfTfx7Sx_yWSv9jeXK-AUJM_J3cffNJDvLV2SnUtqsm0XERTpb-pOrXCZNCSGPnIFX3GtFwZe_J39LebJaJUOYjC9yMn0dk55tbNTXyhQcQabHYE0=s0-d-e1-ft#https://store.fastly.steamstatic.com/public/shared/images/email/logo.png",
    "https://ci3.googleusercontent.com/meips/ADKq_NbdQtxFNDx8gtksu6eKd3LH-cgsuJ85jp6Xyxr4hS1X9NRB2a6sfnZ9AdH09r_U9kWa5yEZEwMCL6-414pOuX3KQ8ND8S-CGOh7wgh6uja3TNNrBiWs-i3QiC3udeWIIniAgJaoI-23L7c9H1An1XS5TO7cr6fZquzhZRV53m0i=s0-d-e1-ft#https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/930210/capsule_616x353.jpg?t=1667495159",
    "https://ci3.googleusercontent.com/meips/ADKq_NaY6nUMATkxG9j0WEMLd7P_sJCdN5y--ElFmxTf7kCVWouFP4zUdZ0jG29zEw93P6Oz2ljQhVOmIy-_Q9a-l_YqdyS79KNhxWgVfXApiEnpqb8AuGyEOXz3bS9MqOQISs-DtW-5KB7v1oYISL2CK709TtWE8ThFJpy7dZarjwul=s0-d-e1-ft#https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/433340/capsule_616x353.jpg?t=1732647440",
    "https://ci3.googleusercontent.com/meips/ADKq_Nb0r51ZTbDZWRQIPO7uDCm-2iUHIr2iahdeeAlVkAcC-7K-HQdo-1Aa6juqhPANSOHJToArqiEc-0TUaLavUJMkNeG47_Z_sjkikhzBeb3K9TP_YfRWdao3TLHCpdp2VRHyXrzqMD8arAuiQY7YqUJOvSxBHM2UBL0VBM86rTR1UQ=s0-d-e1-ft#https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1051200/capsule_616x353.jpg?t=1729043819",
    "https://ci3.googleusercontent.com/meips/ADKq_NZJIC2JBSjMhze-MBGXwWVKf6F8HrWgsvceSVQ6yI_BzV8NXA0QEpjX8phgXKPRS2UV_ZqM9sPxZvxvfjO7FsQ9-nd0sgPpe-cZUkq9af3MmTkUszKVM41E2G8Lq1eFE5OfDbiP=s0-d-e1-ft#https://store.fastly.steamstatic.com/public/shared/images/email/logo_footer.png",
    "https://ci3.googleusercontent.com/meips/ADKq_NYPXiiD1xdxO-VuDkoefXKFCriPR-L50EZ456kU3UmuH6uFLuGb8g-lELUSRmCsBqrmCedFK-m3jGVh8qnDNo1I97N2nbSyT06Xc41Y1hJydfHdZTLbrDn7-EH2ktKYzoxB-w4=s0-d-e1-ft#https://store.fastly.steamstatic.com/public/shared/images/email/logo_valve.jpg",
    "https://ci3.googleusercontent.com/meips/ADKq_NYcUVoMGWTs6tbLLNcP55TKkIZMN5ydD63F1BRr3mAU3yktur9Efp_Fh0eNLIRfoj8zS29TeFnknurb2nlibE_gkeAeLuHi3XQpx9NDL746o4OUzCFn=s0-d-e1-ft#https://cdn.fastly.steamstatic.com/store/email/general/ico_x.png"
    ]
    print(list(process_images(image_urls)))