#!/bin/bash

# Default Django port
PORT="${PORT:-8000}"

echo "Starting ngrok on port $PORT..."
echo "Make sure your Django server is running!"
echo "command: python manage.py runserver"

ngrok http $PORT
