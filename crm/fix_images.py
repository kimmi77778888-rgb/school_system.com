"""
Clear ALL non-Cloudinary image paths from the production database.
On Render, only Cloudinary images work. Local file paths are broken.
Run during every deploy to clean up stale paths.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

if not os.environ.get('DATABASE_URL'):
    print("Local environment — skipping fix_images.py")
    exit(0)

from school.models import Student, Teacher, UserProfile, SchoolSettings

def is_cloudinary(name):
    """Return True only if the name is a Cloudinary URL or path."""
    if not name:
        return False
    # Cloudinary paths look like: image/upload/... or contain cloudinary.com
    return ('cloudinary' in name.lower() or
            name.startswith('http://res.cloudinary') or
            name.startswith('https://res.cloudinary') or
            name.startswith('image/upload/'))

def should_clear(field):
    """Return True if the field has a path that is NOT a valid Cloudinary path."""
    if not field or not field.name:
        return False
    return not is_cloudinary(field.name)

# Clear broken student photos
count = 0
for s in Student.objects.exclude(photo='').exclude(photo=None):
    if should_clear(s.photo):
        Student.objects.filter(pk=s.pk).update(photo='')
        count += 1
print(f"Cleared {count} broken student photos")

# Clear broken teacher photos
count = 0
for t in Teacher.objects.exclude(photo='').exclude(photo=None):
    if should_clear(t.photo):
        Teacher.objects.filter(pk=t.pk).update(photo='')
        count += 1
print(f"Cleared {count} broken teacher photos")

# Clear broken user profile photos
count = 0
for p in UserProfile.objects.exclude(photo='').exclude(photo=None):
    if should_clear(p.photo):
        UserProfile.objects.filter(pk=p.pk).update(photo='')
        count += 1
print(f"Cleared {count} broken user profile photos")

# Clear broken school logo/favicon
s = SchoolSettings.objects.filter(pk=1).first()
if s:
    changed = False
    if should_clear(s.logo):
        s.logo = ''
        changed = True
        print("Cleared broken school logo")
    if should_clear(s.favicon):
        s.favicon = ''
        changed = True
        print("Cleared broken school favicon")
    if changed:
        s.save()

print("fix_images.py complete.")
