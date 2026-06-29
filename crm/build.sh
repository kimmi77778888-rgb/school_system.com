#!/usr/bin/env bash
# Render build script

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create admin user if needed (safe — skips if already exists)
python create_admin.py

# Fix broken image paths from old local uploads (safe — skips on error)
python fix_images.py || true

# Load seed data if available (safe — skips on error)
python load_data.py || true
