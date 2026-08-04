#!/usr/bin/env python
"""
Test Promotion System Calculation
ពិនិត្យការគណនាប្រព័ន្ធឡើងថ្នាក់
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Student, Score, Attendance, Classroom

print('=' * 70)
print('📊 TESTING PROMOTION SYSTEM - SCORE CALCULATION')
print('=' * 70)

# Get students with classrooms
students = Student.objects.filter(is_active=True, classroom__isnull=False)[:3]

print(f'\nពិនិត្យសិស្ស {students.count()} នាក់\n')

for student in students:
    print('-' * 70)
    print(f'សិស្ស: {student} ({student.student_id})')
    print(f'ថ្នាក់: {student.classroom}')
    
    # Get scores
    scores = student.scores.all()
    print(f'ចំនួនមុខវិជ្ជា: {scores.count()}')
    
    if scores.exists():
        # Show individual subject scores
        print('\nពិន្ទុតាមមុខវិជ្ជា:')
        for score in scores[:5]:  # Show first 5
            print(f'  - {score.subject.name}: {score.score}/{score.max_score} ({score.percentage():.1f}%)')
        
        # Calculate average percentage
        total_subjects = scores.count()
        avg_percentage = sum(score.percentage() for score in scores) / total_subjects
        print(f'\n✅ ពិន្ទុមធ្យម: {avg_percentage:.1f}%')
        
        # Check attendance
        attendances = student.attendances.all()
        total_days = attendances.count()
        present_days = attendances.filter(status='P').count()
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        print(f'✅ វត្តមាន: {present_days}/{total_days} ថ្ងៃ ({attendance_rate:.1f}%)')
        
        # Check promotion eligibility
        passing_percentage = 50
        can_promote = (
            avg_percentage >= passing_percentage and 
            total_subjects > 0 and
            attendance_rate >= 80.0
        )
        
        print(f'\nលក្ខខណ្ឌឡើងថ្នាក់:')
        print(f'  - ពិន្ទុ ≥ {passing_percentage}%: {"✅" if avg_percentage >= passing_percentage else "❌"} ({avg_percentage:.1f}%)')
        print(f'  - មានមុខវិជ្ជា ≥ 1: {"✅" if total_subjects > 0 else "❌"} ({total_subjects} មុខ)')
        print(f'  - វត្តមាន ≥ 80%: {"✅" if attendance_rate >= 80.0 else "❌"} ({attendance_rate:.1f}%)')
        
        if can_promote:
            print('\n🎉 លទ្ធផល: ✅ អាចឡើងថ្នាក់បាន')
        else:
            print('\n⚠️  លទ្ធផល: ❌ មិនអាចឡើងថ្នាក់')
            if avg_percentage < passing_percentage:
                print('     មូលហេតុ: ពិន្ទុមធ្យមតិចពេក')
            if attendance_rate < 80:
                print('     មូលហេតុ: វត្តមានតិចពេក')
    else:
        print('❌ មិនមានពិន្ទុក្នុងប្រព័ន្ធ')

print('\n' + '=' * 70)
print('✅ ការពិនិត្យបញ្ចប់!')
print('=' * 70)
print('\nការណែនាំ:')
print('1. បញ្ចូលពិន្ទុក្នុង Grade Book (លទ្ធផលប្រឡង → បញ្ជីពិន្ទុសញ្ញាត្រ)')
print('2. កត់ត្រាវត្តមានប្រចាំថ្ងៃ (វត្តមាន → បញ្ចូលវត្តមាន)')
print('3. ដាក់សិស្សឡើងថ្នាក់ (សិស្ស → ឡើងថ្នាក់)')
print('=' * 70)
