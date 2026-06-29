"""Export local SQLite data to JSON for import into PostgreSQL."""
import os
import sys
import django

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.core import serializers
from django.apps import apps

# Only export these specific models (skip sessions, contenttypes, permissions)
export_models = [
    'auth.user',
    'auth.group',
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

all_objects = []
for label in export_models:
    app_label, model_name = label.split('.')
    try:
        model = apps.get_model(app_label, model_name)
        qs = model.objects.all()
        count = qs.count()
        all_objects.extend(qs)
        print(f"  Exported {count} records from {label}")
    except Exception as e:
        print(f"  Skipped {label}: {e}")

data = serializers.serialize(
    'json', all_objects, indent=2,
    use_natural_foreign_keys=True,
    use_natural_primary_keys=True
)

with open('data_export.json', 'w', encoding='utf-8') as f:
    f.write(data)

print(f"\nDone! Exported to data_export.json")
