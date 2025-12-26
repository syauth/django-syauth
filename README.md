# Django SDK for Syauth

Official Django integration for [Syauth](https://syauth.com).

## Installation

```bash
pip install django-syauth
```

## Configuration

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_syauth',
]
```

Add configuration to `settings.py`:

```python
SYAUTH = {
    'API_URL': 'https://api.syauth.com',
    'CLIENT_ID': 'YOUR_CLIENT_ID',
    'CLIENT_SECRET': 'YOUR_CLIENT_SECRET',
    'REDIRECT_URI': 'http://localhost:8000/auth/callback',
    'SCOPES': ['openid', 'profile', 'email'],
}
```

## Usage

See [documentation](https://docs.syauth.com) for full details.

### Example Project

Check out the [example application](examples/django-app-with-sdk) to see how to integrate the SDK.

