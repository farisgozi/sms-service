#!/bin/bash

# Install Python dependencies
python -m pip install -r requirements.txt

# Verify database connection
echo "Verifying database connection..."
python manage.py check

# Collect static files
python manage.py collectstatic --noinput --clear

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Create superuser if not exists
echo "Setting up superuser..."
echo "from users.models import User; User.objects.create_superuser('admin', 'hexanest@gmail.com', 'hexanestdotaidi') if not User.objects.filter(email='hexanest@gmail.com').exists() else print('Superuser already exists')" | python manage.py shell