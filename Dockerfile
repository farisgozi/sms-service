# Gunakan image Python versi terbaru
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy .env jika ada
COPY .env /app/.env

# Jalankan migrasi dan collectstatic
RUN python manage.py migrate --noinput && python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Jalankan server Django
CMD ["gunicorn", "sms_project.wsgi:application", "--bind", "0.0.0.0:8000"]