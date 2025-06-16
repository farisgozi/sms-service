#!/bin/bash

# ==============================================================================
# Entrypoint Script for Django Application on Dokploy
#
# This script performs the following actions:
# 1. Installs Python dependencies.
# 2. Checks the database connection.
# 3. Collects all static files into a single directory.
# 4. Applies database migrations.
# 5. Creates a superuser if it doesn't already exist.
# 6. Starts the Gunicorn web server to serve the Django application.
# ==============================================================================

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Helper Function for Logging ---
log_message() {
    # Echo a message with a timestamp.
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# --- Step 1: Install Python Dependencies ---
log_message "Installing Python dependencies from requirements.txt..."
python -m pip install -r requirements.txt

# --- Step 2: Verify Database Connection ---
# This command will exit with an error if it cannot connect to the database.
log_message "Verifying database connection..."
python manage.py check

# --- Step 3: Collect Static Files ---
# --noinput: Do not prompt the user for input of any kind.
# --clear: Clear the existing files before trying to copy or link new files.
log_message "Collecting static files..."
python manage.py collectstatic --noinput --clear

# --- Step 4: Run Database Migrations ---
log_message "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# --- Step 5: Create Superuser (Idempotent) ---
# This block runs a Python script within the Django shell.
# It checks if the superuser already exists before attempting to create one,
# preventing errors on subsequent deployments.
log_message "Setting up superuser..."
cat << EOF | python manage.py shell
import os
from users.models import User # IMPORTANT: Change 'users.models' if your User model is elsewhere

# Get credentials from environment variables for better security
SUPERUSER_EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'hexanest@gmail.com')
SUPERUSER_USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
SUPERUSER_PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'hexanestdotaidi')

try:
    if not User.objects.filter(email=SUPERUSER_EMAIL).exists():
        User.objects.create_superuser(
            username=SUPERUSER_USERNAME,
            email=SUPERUSER_EMAIL,
            password=SUPERUSER_PASSWORD
        )
        print('Superuser created successfully.')
    else:
        print('Superuser already exists.')
except Exception as e:
    print(f'Error creating superuser: {str(e)}')
    # Do not exit here, allow the server to start anyway
EOF

# --- Final Step: Start the Application Server ---
log_message "Build process completed. Starting Gunicorn server..."

# IMPORTANT: Replace 'your_project_name' with the name of the directory
# that contains your wsgi.py file.
# The 'exec' command replaces the shell process with the Gunicorn process,
# making it the main process (PID 1) in the container.
exec gunicorn sms_project.wsgi:application --workers 5 --bind 0.0.0.0:8000