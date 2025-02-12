from flask import Blueprint, request, jsonify, abort
from .auth import check_origin, authenticate_token
from .utils import sanitize_content, checkContent
from models import predict_malware, get_file_extension ,TEXT_EXTENSIONS, is_downloadable, extractUrls
import base64, os, warnings, requests

bp = Blueprint('api', __name__, url_prefix='/')

@bp.route('/send_data', methods=['POST'])
def receive_data():
    # Check the 'Origin' header for domain validation
    origin = request.headers.get('Origin')
    if not check_origin(origin):
        abort(403, description="Forbidden: Unauthorized domain")

    # Authenticate request token
    if not authenticate_token(request):
        abort(401, description="Unauthorized access")

    # Ensure the request contains JSON data
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expected application/json"}), 400

    data = request.get_json()

    # Ensure the 'content' field is present
    if 'emailText' not in data:
        return jsonify({"error": "Missing 'EmailText' in the request"}), 400

    # Sanitize the 'content' to avoid XSS attacks
    sanitized_content = sanitize_content(data['emailText'])
    
    # Process the content (e.g., logging or saving to database)
    # print(f"Received content: {sanitized_content}")
    checked = checkContent(sanitized_content, data['urls'], data['imageLinks'])
    checked['attachments'] = dict()
    attachments = data.get('attachments', [])
    saved_files,file_names = [], []
    for attachment in attachments:
        try:
            file_name = attachment['name']
            if get_file_extension(file_name) in TEXT_EXTENSIONS:
                file_data = base64.b64decode(attachment['base64'])
                file_path = os.path.join(r"server/tmp/", file_name) #TODO: move to config

                with open(file_path, 'wb') as f:
                    f.write(file_data)
                file_names.append(file_name)
                saved_files.append(file_path)
            else:
                checked['attachments'].update({file_name:False})
        except Exception as e:
            warnings.warn(f"Error saving {attachment['name']}: {e}")
    
    if downloadable_links:=list(filter(is_downloadable, data['urls']+ extractUrls(sanitized_content))):
        for file_url in downloadable_links:
            try:
                file_name = os.path.basename(file_url)  # Extract filename from URL
                if get_file_extension(file_name) in TEXT_EXTENSIONS:
                    file_path = os.path.join(r"server/tmp/", file_name)

                    response = requests.get(file_url, stream=True)
                    if response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        file_names.append(file_name)
                        saved_files.append(file_path)
                    else:
                        warnings.warn(f"Failed to download: {file_url}, Status Code: {response.status_code}")
                else:
                    checked['attachments'].update({file_name:False})
            except Exception as e:
                warnings.warn(f"Error downloading {file_url}: {e}")
            

    checked['attachments'].update({filename : predict_malware(filepath) for filename, filepath in zip(file_names, saved_files)})
    print(checked)
    for file in saved_files:
        if os.path.exists(file):
            os.remove(file)
    return jsonify(checked), 200
