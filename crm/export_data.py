"""Export local SQLite data to JSON for import into PostgreSQL."""
import os
import sys
import json
import django

# Force UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.core import serializers
from django.apps import apps

exclude_apps = {'contenttypes', 'admin'}
exclude_models = {'auth.permission', 'admin.logentry'}

all_objects = []
for model in apps.get_models():
    label = f"{model._meta.app_label}.{model._meta.model_name}"
    if model._meta.app_label in exclude_apps:
        continue
    if label in exclude_models:
        continue
    try:
        qs = model.objects.all()
        all_objects.extend(qs)
        print(f"  Exported {qs.count()} records from {label}")
    except Exception as e:
        print(f"  Skipped {label}: {e}")

data = serializers.serialize('json', all_objects, indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)

with open('data_export.json', 'w', encoding='utf-8') as f:
    f.write(data)

print(f"\nDone! Exported to data_export.json")
