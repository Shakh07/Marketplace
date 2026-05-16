#!/bin/bash
set -e

echo "Waiting for database..."
until python -c "import psycopg2, os; psycopg2.connect(os.environ.get('DATABASE_URL', ''))" 2>/dev/null; do
    echo "  DB not ready yet, retrying in 2s..."
    sleep 2
done
echo "Database is ready!"

echo "Applying database migrations..."
python manage.py migrate --noinput

export DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-"admin"}
export DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"admin@nexus.uz"}
export DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-"admin123"}

echo "Creating superuser (Admin)..."
python manage.py createsuperuser --noinput || true

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating media directories..."
mkdir -p /app/media/products /app/media/products/thumbs /app/media/categories /app/media/hero /app/media/brands /app/media/profiles 2>/dev/null || true

echo "Starting Gunicorn..."
exec gunicorn ecommerce.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

