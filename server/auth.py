import re
from flask import request
from .config import Config

def check_origin(origin):
    """Check if the request comes from an allowed domain."""
    if origin:
        domain = re.sub(r'^https:\/\/', '', origin).split('/')[0] #allow only https
        return any(domain.endswith(email_domain) for email_domain in Config.ALLOWED_DOMAINS)
    return False

def authenticate_token(request):
    """Authenticate the request by checking the API token."""
    token = request.headers.get('Authorization')
    return token == f'Bearer {Config.API_TOKEN}'
