"""
Django Management Command: Scan System for Problems
====================================================
Usage: python manage.py scan_system [options]

Options:
  --full          Run all checks (default)
  --quick         Quick scan (essential checks only)
  --templates     Check templates for encoding issues
  --database      Check database integrity
  --models        Check model data quality
  --urls          Check URL configuration
  --static        Check static/media files
  --security      Check security settings
  --performance   Check performance issues
  --fix           Auto-fix simple issues (use with caution)
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.contrib.auth.models import User
from school.models import (
    Student, Teacher, Classroom, AcademicYear, Subject, Score,
    Attendance, Exam, Notification, ReportCard
)
from django.conf import settings
from django.urls import get_resolver
import os
import re
from collections import defaultdict


class Command(BaseCommand):
    help = 'Scan system for problems and report issues'

    def add_arguments(self, parser):
        parser.add_argument('--full', action='store_true', help='Run all checks')
        parser.add_argument('--quick', action='store_true', help='Quick essential checks only')
        parser.add_argument('--templates', action='store_true', help='Check templates')
        parser.add_argument('--database', action='store_true', help='Check database')
        parser.add_argument('--models', action='store_true', help='Check models')
        parser.add_argument('--urls', action='store_true', help='Check URLs')
        parser.add_argument('--static', action='store_true', help='Check static files')
        parser.add_argument('--security', action='store_true', help='Check security')
        parser.add_argument('--performance', action='store_true', help='Check performance')
        parser.add_argument('--fix', action='store_true', help='Auto-fix simple issues')

    def handle(self, *args, **options):
        self.fix_mode = options['fix']
        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        self.fixes_applied = []
        
        # Determine what to scan
        if options['quick']:
            checks = ['database', 'models', 'templates']
        elif options['full'] or not any([options[k] for k in ['templates', 'database', 'models', 'urls', 'static', 'security', 'performance']]):
            checks = ['database', 'templates', 'models', 'urls', 'static', 'security', 'performance']
        else:
            checks = [k for k in ['templates', 'database', 'models', 'urls', 'static', 'security', 'performance'] if options[k]]
        
        self.stdout.write("\n" + "="*70)
        self.stdout.write(self.style.SUCCESS("  SYSTEM PROBLEM SCANNER"))
        self.stdout.write("="*70 + "\n")
        
        if self.fix_mode:
            self.stdout.write(self.style.WARNING("⚠️  AUTO-FIX MODE ENABLED\n"))
        
        # Run selected checks
        if 'database' in checks:
            self.check_database()
        if 'templates' in checks:
            self.check_templates()
        if 'models' in checks:
            self.check_models()
        if 'urls' in checks:
            self.check_urls()
        if 'static' in checks:
            self.check_static_files()
        if 'security' in checks:
            self.check_security()
        if 'performance' in checks:
            self.check_performance()
        
        # Display summary
        self.display_summary()

    def print_header(self, title):
        self.stdout.write(f"\n{'─'*70}")
        self.stdout.write(self.style.HTTP_INFO(f"  {title}"))
        self.stdout.write("─"*70 + "\n")

    def check_database(self):
        """Check database connectivity and integrity"""
        self.print_header("DATABASE CHECK")
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                self.stdout.write(self.style.SUCCESS(f"✓ Database connected ({len(tables)} tables)"))
                
                # Check for orphaned records
                orphaned_students = Student.objects.filter(classroom__isnull=True, is_active=True)
                if orphaned_students.exists():
                    self.warnings['database'].append(f"{orphaned_students.count()} active students without classroom")
                
                # Check for missing relationships
                classrooms_no_teacher = Classroom.objects.filter(homeroom_teacher__isnull=True)
                if classrooms_no_teacher.exists():
                    self.warnings['database'].append(f"{classrooms_no_teacher.count()} classrooms without homeroom teacher")
                
                # Check for inactive academic years with active classrooms
                for year in AcademicYear.objects.filter(is_active=False):
                    active_classrooms = year.classrooms.filter(students__is_active=True).distinct().count()
                    if active_classrooms > 0:
                        self.warnings['database'].append(f"Inactive year '{year.year}' has {active_classrooms} classrooms with active students")
                
                if not self.warnings['database']:
                    self.stdout.write(self.style.SUCCESS("✓ No database issues found"))
                    
        except Exception as e:
            self.issues['database'].append(f"Connection error: {str(e)}")

    def check_templates(self):
        """Check for template issues"""
        self.print_header("TEMPLATE CHECK")
        
        template_dir = os.path.join('school', 'templates')
        total = 0
        encoding_issues = []
        syntax_issues = []
        
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    total += 1
                    filepath = os.path.join(root, file)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                            # Check encoding
                            qmark_count = len(re.findall(r'\?{6,}', content))
                            if qmark_count > 0:
                                encoding_issues.append((file, qmark_count))
                                if self.fix_mode:
                                    self.stdout.write(self.style.WARNING(f"⚠️  Cannot auto-fix encoding in {file}"))
                            
                            # Remove CSS/JS content before checking Django template tags
                            # to avoid false positives from CSS curly braces
                            content_no_css = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
                            content_no_js = re.sub(r'<script[^>]*>.*?</script>', '', content_no_css, flags=re.DOTALL)
                            
                            # Check for common syntax errors in Django template tags only
                            if content_no_js.count('{%') != content_no_js.count('%}'):
                                syntax_issues.append((file, "Unbalanced template tags"))
                            if content_no_js.count('{{') != content_no_js.count('}}'):
                                syntax_issues.append((file, "Unbalanced variable tags"))
                            
                    except Exception as e:
                        self.issues['templates'].append(f"{file}: {str(e)}")
        
        self.stdout.write(f"Scanned {total} templates")
        
        if encoding_issues:
            self.issues['templates'].extend([f"{f}: {c} encoding issues" for f, c in encoding_issues])
        if syntax_issues:
            self.issues['templates'].extend([f"{f}: {issue}" for f, issue in syntax_issues])
        
        if not self.issues['templates']:
            self.stdout.write(self.style.SUCCESS("✓ All templates OK"))

    def check_models(self):
        """Check model data quality"""
        self.print_header("MODEL DATA CHECK")
        
        # Check Students
        students = Student.objects.all()
        for student in students:
            if not student.first_name or not student.last_name:
                self.issues['models'].append(f"Student {student.student_id}: Missing name")
            
            if student.student_id and not student.student_id.startswith('STU-'):
                self.warnings['models'].append(f"Student {student.student_id}: Non-standard ID format (cannot auto-fix)")
            
            if student.is_active and not student.classroom:
                self.warnings['models'].append(f"Student {student.student_id}: Active but no classroom")
        
        # Check Teachers
        teachers = Teacher.objects.all()
        for teacher in teachers:
            if not teacher.first_name or not teacher.last_name:
                self.issues['models'].append(f"Teacher {teacher.teacher_id}: Missing name")
            
            if teacher.is_active and not teacher.phone and not teacher.email:
                self.warnings['models'].append(f"Teacher {teacher.teacher_id}: No contact information")
        
        # Check for duplicate IDs
        student_ids = Student.objects.values_list('student_id', flat=True)
        duplicates = [id for id in student_ids if student_ids.filter(student_id=id).count() > 1]
        if duplicates:
            self.issues['models'].append(f"Duplicate student IDs found: {', '.join(set(duplicates))}")
        
        if not self.issues['models'] and not self.warnings['models']:
            self.stdout.write(self.style.SUCCESS("✓ Model data is clean"))

    def check_urls(self):
        """Check URL configuration"""
        self.print_header("URL CHECK")
        
        try:
            resolver = get_resolver()
            patterns = list(resolver.url_patterns)
            self.stdout.write(self.style.SUCCESS(f"✓ {len(patterns)} URL patterns loaded"))
            
            # Check for common patterns
            required_patterns = ['student_list', 'teacher_list', 'dashboard']
            missing = []
            for pattern_name in required_patterns:
                found = False
                for p in patterns:
                    if hasattr(p, 'url_patterns'):
                        for sub in p.url_patterns:
                            if hasattr(sub, 'name') and pattern_name in str(sub.name):
                                found = True
                                break
                if not found:
                    missing.append(pattern_name)
            
            if missing:
                self.warnings['urls'].append(f"Could not verify patterns: {', '.join(missing)}")
            else:
                self.stdout.write(self.style.SUCCESS("✓ Essential URL patterns found"))
                
        except Exception as e:
            self.issues['urls'].append(f"URL configuration error: {str(e)}")

    def check_static_files(self):
        """Check static and media files"""
        self.print_header("STATIC & MEDIA CHECK")
        
        checks = [
            ('staticfiles', 'Static files', False),
            ('images', 'Media images', False),
            ('documents', 'Documents', True),
        ]
        
        for dirname, label, can_create in checks:
            if os.path.exists(dirname):
                file_count = sum([len(files) for r, d, files in os.walk(dirname)])
                self.stdout.write(self.style.SUCCESS(f"✓ {label}: {file_count} files"))
            else:
                self.warnings['static'].append(f"{label} directory missing: {dirname}/")
                if self.fix_mode and can_create:
                    os.makedirs(dirname, exist_ok=True)
                    self.fixes_applied.append(f"Created {dirname}/ directory")

    def check_security(self):
        """Check security settings"""
        self.print_header("SECURITY CHECK")
        
        # Check DEBUG mode
        if settings.DEBUG:
            self.warnings['security'].append("DEBUG mode is ON (should be OFF in production)")
        else:
            self.stdout.write(self.style.SUCCESS("✓ DEBUG mode is OFF"))
        
        # Check SECRET_KEY
        if settings.SECRET_KEY == 'your-secret-key-here' or len(settings.SECRET_KEY) < 50:
            self.issues['security'].append("SECRET_KEY is weak or default")
        
        # Check ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
            self.warnings['security'].append("ALLOWED_HOSTS is not properly configured")
        
        # Check for sensitive data in .env
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                env_content = f.read()
                if 'password' in env_content.lower() or 'secret' in env_content.lower():
                    self.stdout.write(self.style.SUCCESS("✓ .env file contains credentials (ensure .gitignore blocks it)"))
        
        if not self.issues['security']:
            self.stdout.write(self.style.SUCCESS("✓ No critical security issues"))

    def check_performance(self):
        """Check performance issues"""
        self.print_header("PERFORMANCE CHECK")
        
        # Check for N+1 query issues in models
        warnings = []
        
        # Check if select_related/prefetch_related is needed
        large_querysets = [
            (Student.objects.all(), "Students", ['classroom']),
            (Score.objects.all(), "Scores", ['student', 'subject']),
            (Classroom.objects.all(), "Classrooms", ['grade', 'academic_year']),
        ]
        
        for qs, name, related_fields in large_querysets:
            count = qs.count()
            if count > 100:
                warnings.append(f"{name}: {count} records (consider pagination)")
        
        # Check database size
        if os.path.exists('db.sqlite3'):
            size_mb = os.path.getsize('db.sqlite3') / (1024 * 1024)
            if size_mb > 100:
                warnings.append(f"Database size: {size_mb:.1f}MB (consider optimization)")
            else:
                self.stdout.write(self.style.SUCCESS(f"✓ Database size: {size_mb:.1f}MB"))
        
        if warnings:
            self.warnings['performance'].extend(warnings)
        else:
            self.stdout.write(self.style.SUCCESS("✓ No performance issues detected"))

    def display_summary(self):
        """Display summary of all issues found"""
        self.stdout.write("\n" + "="*70)
        self.stdout.write(self.style.HTTP_INFO("  SCAN SUMMARY"))
        self.stdout.write("="*70 + "\n")
        
        # Count issues
        total_issues = sum(len(issues) for issues in self.issues.values())
        total_warnings = sum(len(warnings) for warnings in self.warnings.values())
        
        # Display critical issues
        if total_issues > 0:
            self.stdout.write(self.style.ERROR(f"\n❌ CRITICAL ISSUES FOUND: {total_issues}\n"))
            for category, issue_list in self.issues.items():
                if issue_list:
                    self.stdout.write(self.style.ERROR(f"\n{category.upper()}:"))
                    for issue in issue_list:
                        self.stdout.write(f"  ❌ {issue}")
        else:
            self.stdout.write(self.style.SUCCESS("\n✓ NO CRITICAL ISSUES FOUND\n"))
        
        # Display warnings
        if total_warnings > 0:
            self.stdout.write(self.style.WARNING(f"\n⚠️  WARNINGS: {total_warnings}\n"))
            for category, warning_list in self.warnings.items():
                if warning_list:
                    self.stdout.write(self.style.WARNING(f"\n{category.upper()}:"))
                    for warning in warning_list:
                        self.stdout.write(f"  ⚠️  {warning}")
        
        # Display fixes applied
        if self.fixes_applied:
            self.stdout.write(self.style.SUCCESS(f"\n\n🔧 FIXES APPLIED: {len(self.fixes_applied)}\n"))
            for fix in self.fixes_applied:
                self.stdout.write(f"  ✓ {fix}")
        
        # Overall status
        self.stdout.write("\n" + "="*70)
        if total_issues == 0 and total_warnings == 0:
            self.stdout.write(self.style.SUCCESS("\n🎉 SYSTEM IS HEALTHY!\n"))
        elif total_issues == 0:
            self.stdout.write(self.style.WARNING(f"\n⚠️  System operational with {total_warnings} warning(s)\n"))
        else:
            self.stdout.write(self.style.ERROR(f"\n❌ {total_issues} critical issue(s) need attention\n"))
        
        self.stdout.write("="*70 + "\n")
