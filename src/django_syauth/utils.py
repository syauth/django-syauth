import hashlib
import base64
import os
import requests
import jwt
from django.conf import settings
from urllib.parse import urlencode

def get_config():
    """Retrieve Syauth configuration from Django settings."""
    config = getattr(settings, 'SYAUTH', {})
    required_keys = ['API_URL', 'CLIENT_ID', 'REDIRECT_URI']
    
    missing = [key for key in required_keys if key not in config]
    if missing:
        raise ValueError(f"Missing required SYAUTH settings: {', '.join(missing)}")
        
    return config

def generate_pkce_pair():
    """Generate a PKCE code verifier and code challenge."""
    # Generate a random 32-byte state
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').rstrip('=')
    
    # Create code challenge
    m = hashlib.sha256()
    m.update(code_verifier.encode('utf-8'))
    code_challenge = base64.urlsafe_b64encode(m.digest()).decode('utf-8').rstrip('=')
    
    return code_verifier, code_challenge

def get_authorization_url(state, code_challenge):
    """Build the authorization URL."""
    config = get_config()
    params = {
        'client_id': config['CLIENT_ID'],
        'response_type': 'code',
        'redirect_uri': config['REDIRECT_URI'],
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'scope': ' '.join(config.get('SCOPES', ['openid', 'profile', 'email'])),
    }
    
    # Add API Key if present (required for some environments)
    if 'API_KEY' in config:
        params['api_key'] = config['API_KEY']
    
    # Construct base URL correctly handling trailing slashes
    base_url = config['API_URL'].rstrip('/')
    return f"{base_url}/oauth/authorize/?{urlencode(params)}"

def exchange_code_for_token(code, code_verifier):
    """Exchange authorization code for tokens."""
    config = get_config()
    
    token_url = f"{config['API_URL'].rstrip('/')}/oauth/token/"
    payload = {
        'grant_type': 'authorization_code',
        'client_id': config['CLIENT_ID'],
        'client_secret': config.get('CLIENT_SECRET', ''),
        'code': code,
        'redirect_uri': config['REDIRECT_URI'],
        'code_verifier': code_verifier,
    }
    
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()

def decode_id_token(id_token):
    """Decode and validate the ID token (simple decoding for now)."""
    # In production, this should verify the signature using JWKS
    # For now, we decode without verification to get user info
    return jwt.decode(id_token, options={"verify_signature": False})
