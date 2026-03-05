#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==> Starting build process..."

# Install Python dependencies
echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r minor/requirements_production.txt

# Navigate to Django project directory
cd minor

# Collect static files
echo "==> Collecting static files..."
python manage.py collectstatic --no-input --settings=minor.settings_production

# Run migrations
echo "==> Running database migrations..."
python manage.py migrate --no-input --settings=minor.settings_production

echo "==> Build completed successfully!"
