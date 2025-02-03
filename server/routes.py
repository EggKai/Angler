from flask import Blueprint, request, jsonify, abort
from .auth import check_origin, authenticate_token
from .utils import sanitize_content, checkContent
import base64, os, warnings

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
    print(f"Received content: {sanitized_content}")

    attachments = data.get('attachments', [])

    saved_files = []
    
    for attachment in attachments:
        try:
            file_name = attachment['name']
            file_data = base64.b64decode(attachment['base64'])
            file_path = os.path.join(r"server/tmp/", file_name) #TODO: move to config

            with open(file_path, 'wb') as f:
                f.write(file_data)

            saved_files.append(file_path)
        except Exception as e:
            warnings.warn(f"Error saving {attachment['name']}: {e}")
    checked = checkContent(sanitized_content, data['urls'], data['imageLinks'], saved_files)

    return jsonify(checked), 200
