#!/bin/bash

# Enable error handling
set -e

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Install Python dependencies
log_message "Installing Python dependencies..."
python -m pip install -r requirements.txt

# Verify database connection
log_message "Verifying database connection..."
python manage.py check

# Collect static files
log_message "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run database migrations
log_message "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if not exists
log_message "Setting up superuser..."
cat << EOF | python manage.py shell
try:
    from users.models import User
    if not User.objects.filter(email='hexanest@gmail.com').exists():
        User.objects.create_superuser('admin', 'hexanest@gmail.com', 'hexanestdotaidi')
        print('Superuser created successfully')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {str(e)}')
    exit(1)
EOF

log_message "Build process completed successfully"