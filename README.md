# Django SDK for Syauth

[![PyPI version](https://badge.fury.io/py/django-syauth.svg)](https://badge.fury.io/py/django-syauth)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Django integration for [Syauth](https://syauth.com) - a modern authentication platform.

## Features

- 🔐 OAuth 2.0 Authorization Code Flow with PKCE
- 🚀 Drop-in views for Login, Callback, and Logout
- 🔒 Secure token management
- 🛡️ Protected routes with decorators
- 🎨 Easy integration with Django's authentication system

## Installation

```bash
pip install django-syauth
```

## Quick Start

### 1. Add to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'django_syauth',
]
```

### 2. Configure Authentication Backends

```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django_syauth.backend.SyauthBackend',
]
```

### 3. Add Syauth Settings

```python
SYAUTH = {
    'API_URL': 'https://api.syauth.com/e/v1',
    'CLIENT_ID': 'your-client-id',
    'REDIRECT_URI': 'http://localhost:8000/auth/callback',
    'API_KEY': 'your-api-key',
    'SCOPES': ['openid', 'profile', 'email'],
    # 'CLIENT_SECRET': 'your-secret',  # Only for server-to-server clients
}
```

### 4. Include URLs

```python
from django.urls import path, include

urlpatterns = [
    path('auth/', include('django_syauth.urls')),
    # ... your other urls
]
```

## Usage

### Protecting Views

Use the `@syauth_login_required` decorator to protect views:

```python
from django_syauth.decorators import syauth_login_required

@syauth_login_required
def dashboard(request):
    return render(request, 'dashboard.html')
```

### Template URLs

In your templates, use the named URLs:

```html
<a href="{% url 'django_syauth:login' %}">Sign In</a>
<a href="{% url 'django_syauth:logout' %}">Sign Out</a>
```

### Accessing User Info

After login, user information is available via `request.user`:

```python
def profile(request):
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name
    # ...
```

## Configuration Options

| Setting | Required | Description |
|---------|----------|-------------|
| `API_URL` | ✅ | Syauth API URL (e.g., `https://api.syauth.com/e/v1`) |
| `CLIENT_ID` | ✅ | Your OAuth Client ID |
| `REDIRECT_URI` | ✅ | Callback URL (must match Syauth Dashboard) |
| `API_KEY` | ✅ | Your API Key from Syauth Dashboard |
| `SCOPES` | ❌ | OAuth scopes (default: `['openid', 'profile', 'email']`) |
| `CLIENT_SECRET` | ❌ | Only for server-to-server (confidential) clients |

## Example Application

Check out the [example application](examples/django-app-with-sdk) for a complete working demo.

### Running the Example

```bash
cd examples/django-app-with-sdk

# Copy and configure environment
cp .env.example .env
# Edit .env with your Syauth credentials

# Install dependencies
pip install django requests pyjwt[crypto]

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

## Using with ngrok

For development with external OAuth providers, you may need to use ngrok. See the [ngrok guide](examples/django-app-with-sdk/NGROK.md) for setup instructions.

## Documentation

Full documentation is available at [developers.nexorix.com/syauth](https://developers.nexorix.com/syauth).

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- 📚 [Documentation](https://developers.nexorix.com/syauth)
- 🐛 [Report Issues](https://github.com/nexorix/django-syauth/issues)
- 💬 [Discussions](https://github.com/nexorix/django-syauth/discussions)
