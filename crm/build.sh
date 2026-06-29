#!/usr/bin/env bash
# Render build script

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python create_admin.py

# Load initial data if fixture exists
if [ -f data_export.json ]; then
  python manage.py loaddata data_export.json --ignorenonexistent || echo "Warning: some data skipped"
fi
