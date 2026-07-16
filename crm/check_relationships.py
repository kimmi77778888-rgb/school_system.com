#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth.models import User
from school.models import Teacher, UserProfile, Classroom, Student

print('=== All Users ===')
users = User.objects.all()
for u in users:
    profile_role = u.profile.role if hasattr(u, 'profile') else 'NO PROFILE'
    teacher_link = u.profile.teacher if hasattr(u, 'profile') and u.profile.teacher else None
    print(f'ID: {u.id} | Username: {u.username} | Role: {profile_role} | Teacher: {teacher_link}')

print('\n=== All Teachers ===')
teachers = Teacher.objects.all()
for t in teachers:
    has_profile = hasattr(t, 'user_profile') and t.user_profile is not None
    profile = t.user_profile if has_profile else None
    print(f'ID: {t.id} | {t.first_name} {t.last_name} | Has Profile: {has_profile} | Profile: {profile}')
    
print('\n=== Classrooms with Homeroom Teachers ===')
classrooms = Classroom.objects.all()
for c in classrooms:
    student_count = c.students.filter(is_active=True).count()
    print(f'{c} | Teacher: {c.homeroom_teacher} | Students: {student_count}')
