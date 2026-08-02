#!/usr/bin/env python
"""
System Health Check Script
Run comprehensive checks on the Django CRM system
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from school.models import Student, Teacher, Classroom, AcademicYear, Subject, Score
from django.contrib.auth.models import User
import re

def print_header(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def check_database():
    """Check database connectivity and tables"""
    print_header("DATABASE CHECK")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print(f"✓ Database connected")
            print(f"✓ Total tables: {len(tables)}")
            
            # Check key models
            print(f"\nData counts:")
            print(f"  - Users: {User.objects.count()}")
            print(f"  - Students: {Student.objects.count()}")
            print(f"  - Teachers: {Teacher.objects.count()}")
            print(f"  - Classrooms: {Classroom.objects.count()}")
            print(f"  - Academic Years: {AcademicYear.objects.count()}")
            print(f"  - Subjects: {Subject.objects.count()}")
            print(f"  - Scores: {Score.objects.count()}")
            
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_templates():
    """Check for template encoding issues"""
    print_header("TEMPLATE CHECK")
    
    template_dir = os.path.join('school', 'templates')
    issues = []
    total = 0
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                total += 1
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Check for question marks (encoding issues)
                        qmark_count = len(re.findall(r'\?{6,}', content))
                        if qmark_count > 0:
                            issues.append((file, qmark_count))
                except Exception as e:
                    issues.append((file, f"Read error: {e}"))
    
    print(f"Total HTML templates: {total}")
    
    if issues:
        print(f"\n❌ Found {len(issues)} template(s) with encoding issues:")
        for file, count in issues:
            print(f"  - {file}: {count} issue(s)")
        return False
    else:
        print("✓ All templates have proper encoding")
        return True

def check_models():
    """Check model integrity"""
    print_header("MODEL CHECK")
    
    try:
        # Check Student model
        students = Student.objects.all()
        students_with_issues = []
        
        for student in students[:10]:  # Check first 10
            issues = []
            if not student.first_name:
                issues.append("missing first_name")
            if not student.last_name:
                issues.append("missing last_name")
            if student.student_id and not student.student_id.startswith('STU-'):
                issues.append("invalid student_id format")
            
            if issues:
                students_with_issues.append((student.student_id, issues))
        
        if students_with_issues:
            print(f"⚠ Found {len(students_with_issues)} student(s) with data issues:")
            for sid, issues in students_with_issues:
                print(f"  - {sid}: {', '.join(issues)}")
        else:
            print("✓ Student model data looks good")
        
        # Check Teacher model
        teachers = Teacher.objects.all()
        if teachers.exists():
            print(f"✓ Teacher model OK ({teachers.count()} records)")
        
        return True
        
    except Exception as e:
        print(f"❌ Model check error: {e}")
        return False

def check_urls():
    """Check URL configuration"""
    print_header("URL CHECK")
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        patterns = list(resolver.url_patterns)
        
        print(f"✓ URL configuration loaded")
        print(f"✓ Total URL patterns: {len(patterns)}")
        
        # Check for school URLs
        school_urls = [p for p in patterns if 'school' in str(p.pattern)]
        if school_urls:
            print(f"✓ School app URLs configured")
        
        return True
        
    except Exception as e:
        print(f"❌ URL check error: {e}")
        return False

def check_static_media():
    """Check static and media files"""
    print_header("STATIC & MEDIA CHECK")
    
    checks = [
        ('staticfiles', 'Static files'),
        ('images', 'Media files'),
        ('documents', 'Documents'),
    ]
    
    all_ok = True
    for dirname, label in checks:
        if os.path.exists(dirname):
            file_count = sum([len(files) for r, d, files in os.walk(dirname)])
            print(f"✓ {label}: {dirname}/ ({file_count} files)")
        else:
            print(f"⚠ {label}: {dirname}/ (missing)")
            all_ok = False
    
    return all_ok

def check_name_display():
    """Check if names are displaying in correct order"""
    print_header("NAME DISPLAY CHECK")
    
    try:
        # Check Student __str__ method
        student = Student.objects.first()
        if student:
            student_str = str(student)
            # Should be: STU-XXXX - Last First
            if ' - ' in student_str:
                name_part = student_str.split(' - ', 1)[1]
                expected = f"{student.last_name} {student.first_name}"
                if name_part == expected:
                    print(f"✓ Student __str__ displays correctly: {student_str}")
                else:
                    print(f"⚠ Student __str__ may be wrong order")
                    print(f"  Got: {name_part}")
                    print(f"  Expected: {expected}")
        
        # Check Teacher __str__ method
        teacher = Teacher.objects.first()
        if teacher:
            teacher_str = str(teacher)
            expected = f"{teacher.last_name} {teacher.first_name}"
            if teacher_str == expected:
                print(f"✓ Teacher __str__ displays correctly: {teacher_str}")
            else:
                print(f"⚠ Teacher __str__ may be wrong order")
                print(f"  Got: {teacher_str}")
                print(f"  Expected: {expected}")
        
        return True
        
    except Exception as e:
        print(f"❌ Name display check error: {e}")
        return False

def main():
    """Run all checks"""
    print("\n" + "="*70)
    print("  SCHOOL MANAGEMENT SYSTEM - HEALTH CHECK")
    print("="*70)
    
    results = []
    
    results.append(("Database", check_database()))
    results.append(("Templates", check_templates()))
    results.append(("Models", check_models()))
    results.append(("URLs", check_urls()))
    results.append(("Static/Media", check_static_media()))
    results.append(("Name Display", check_name_display()))
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    for check_name, status in results:
        icon = "✓" if status else "❌"
        print(f"{icon} {check_name}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 System is healthy!")
        return 0
    else:
        print(f"\n⚠ {total - passed} check(s) failed - review above")
        return 1

if __name__ == '__main__':
    sys.exit(main())
