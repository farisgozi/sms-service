#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create superuser if not exists
echo "from users.models import User; User.objects.create_superuser('admin', 'hexanest@gmail.com', 'hexanestdotaidi') if not User.objects.filter(email='hexanest@gmail.com').exists() else None" | python manage.py shell