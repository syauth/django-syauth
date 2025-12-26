# Django Syauth Example Application

A complete example Django application demonstrating the `django-syauth` SDK.

## Features

- User authentication via Syauth
- Protected dashboard and profile pages
- Profile update functionality
- Password change functionality
- Responsive UI

## Prerequisites

- Python 3.8+
- A Syauth account with an OAuth application configured

## Setup

### 1. Install Dependencies

```bash
pip install django requests pyjwt[crypto]
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your Syauth credentials
```

Required environment variables:
- `SYAUTH_CLIENT_ID` - Your OAuth Client ID
- `SYAUTH_API_KEY` - Your API Key
- `SYAUTH_REDIRECT_URI` - Your callback URL (must match Syauth Dashboard)

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start the Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the application.

## Using with ngrok

For external OAuth providers (like Google), you may need a public URL. See [NGROK.md](NGROK.md) for setup instructions.

## Project Structure

```
myapp/
├── settings.py      # Django settings with Syauth config
├── urls.py          # URL routing
├── views.py         # View functions
├── static/
│   └── css/
│       └── style.css
└── templates/
    ├── base.html
    ├── home.html
    ├── dashboard.html
    └── profile.html
```

## License

MIT License - see [LICENSE](../../LICENSE) for details.
