#!/usr/bin/env python
"""
Test script to verify teacher can see their students
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth.models import User
from school.models import Teacher, UserProfile, Classroom, Student

def test_teacher_access():
    print('=== Testing Teacher Access to Students ===\n')
    
    # Get teacher user
    teacher_user = User.objects.get(username='lensophara')
    print(f'Teacher User: {teacher_user.username}')
    print(f'Profile Role: {teacher_user.profile.role}')
    print(f'Linked Teacher: {teacher_user.profile.teacher}')
    
    # Get teacher record
    teacher = teacher_user.profile.teacher
    print(f'\nTeacher: {teacher.first_name} {teacher.last_name}')
    
    # Get classrooms where this teacher is homeroom teacher
    my_classes = Classroom.objects.filter(homeroom_teacher=teacher)
    print(f'\nMy Classrooms ({my_classes.count()}):')
    for c in my_classes:
        print(f'  - {c}')
    
    # Get students in those classrooms
    my_students = Student.objects.filter(classroom__in=my_classes, is_active=True)
    print(f'\nMy Students ({my_students.count()}):')
    for s in my_students:
        print(f'  - {s.student_id}: {s.first_name} {s.last_name} (Classroom: {s.classroom})')
    
    print('\n' + '='*50)
    
    # Test second teacher
    print('\n=== Testing Second Teacher ===\n')
    teacher_user2 = User.objects.get(username='taki')
    print(f'Teacher User: {teacher_user2.username}')
    teacher2 = teacher_user2.profile.teacher
    print(f'Teacher: {teacher2.first_name} {teacher2.last_name}')
    
    my_classes2 = Classroom.objects.filter(homeroom_teacher=teacher2)
    print(f'\nMy Classrooms ({my_classes2.count()}):')
    for c in my_classes2:
        print(f'  - {c}')
    
    my_students2 = Student.objects.filter(classroom__in=my_classes2, is_active=True)
    print(f'\nMy Students ({my_students2.count()}):')
    for s in my_students2:
        print(f'  - {s.student_id}: {s.first_name} {s.last_name} (Classroom: {s.classroom})')

if __name__ == '__main__':
    test_teacher_access()
    print('\n✓ Teacher access test complete!')
    print('\nTeachers can login with:')
    print('  Username: lensophara | Password: teacher123')
    print('  Username: taki | Password: teacher123')
