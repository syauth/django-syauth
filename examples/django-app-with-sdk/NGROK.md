# Running with Ngrok

This guide explains how to run the Django app with ngrok for local development with public URLs.

## Prerequisites

1. Sign up for a free ngrok account at https://dashboard.ngrok.com
2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken
3. Install ngrok CLI.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt # if you have one
# or
pip install django requests "pyjwt[crypto]"
```

## Running with Ngrok

1. **Start your Django Server** in one terminal:

```bash
python manage.py runserver
```

2. **Start Ngrok** in a second terminal:

```bash
./scripts/start-ngrok.sh
```

This will start an ngrok tunnel on port 8000.

## Important Notes

1. **Update settings.py**:
   We have already configured `settings.py` to allow ngrok domains:
   ```python
   CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.app']
   ALLOWED_HOSTS = ['*']
   ```

2. **Update OAuth Redirect URI**:
   When ngrok starts, copy the forwarding URL (e.g., `https://abc123.ngrok-free.app`).
   
   Update your `settings.py`:
   ```python
   SYAUTH = {
       ...
       'REDIRECT_URI': 'https://abc123.ngrok-free.app/auth/callback/',
   }
   ```
   *Don't forget the trailing slash if your Django URL pattern expects it!*

3. **Restart Django**:
   After updating `settings.py`, Django usually reloads automatically, but if you change the redirect URI validation fails, restart just in case.
