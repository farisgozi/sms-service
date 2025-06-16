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