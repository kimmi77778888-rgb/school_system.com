"""
Load fixture data into the database, skipping duplicates.
Run this during Render deployment.
"""
import os
import sys
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.apps import apps
from django.core import serializers

# Only run if DATABASE_URL is set (we're on Render/PostgreSQL)
if not os.environ.get('DATABASE_URL'):
    print("No DATABASE_URL found — skipping data load (local dev mode)")
    sys.exit(0)

if not os.path.exists('data_export.json'):
    print("No data_export.json found — skipping")
    sys.exit(0)

print("Loading data from data_export.json...")

with open('data_export.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load in correct order to respect foreign keys
model_order = [
    'auth.group',
    'auth.user',
    'school.schoolsettings',
    'school.academicyear',
    'school.grade',
    'school.teacher',
    'school.classroom',
    'school.student',
    'school.subject',
    'school.timeslot',
    'school.timetable',
    'school.examtype',
    'school.exam',
    'school.score',
    'school.attendance',
    'school.notification',
    'school.schoolevent',
    'school.reportcard',
    'school.userprofile',
]

total_created = 0
total_skipped = 0

for model_label in model_order:
    app_label, model_name = model_label.split('.')
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        continue

    records = [item for item in data if item['model'] == model_label]
    if not records:
        continue

    created = 0
    skipped = 0
    for record in records:
        json_str = json.dumps([record], ensure_ascii=False)
        try:
            for obj in serializers.deserialize('json', json_str):
                try:
                    # Check if already exists
                    if model.objects.filter(pk=obj.object.pk).exists():
                        skipped += 1
                    else:
                        obj.save()
                        created += 1
                except Exception as e:
                    skipped += 1
        except Exception as e:
            skipped += 1

    print(f"  {model_label}: {created} created, {skipped} skipped")
    total_created += created
    total_skipped += skipped

print(f"\nDone! Total: {total_created} created, {total_skipped} skipped")
