#!/bin/bash

# Menjalankan migrasi database
python manage.py migrate

# Membuat superuser secara otomatis
echo "from users.models import User; User.objects.create_superuser('admin', 'hexanest@gmail.com', 'hexanestdotaidi') if not User.objects.filter(email='hexanest@gmail.com').exists() else None" | python manage.py shell