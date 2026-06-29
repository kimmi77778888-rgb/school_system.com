import django, os, traceback
os.environ['DJANGO_SETTINGS_MODULE'] = 'crm.settings'
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from school.models import UserProfile, Student, Teacher, Classroom, AcademicYear, Grade

def mu(u, r):
    usr, _ = User.objects.get_or_create(username=u)
    usr.set_password('x'); usr.save()
    UserProfile.objects.update_or_create(user=usr, defaults={'role': r})
    return usr

admin = User.objects.get(username='admin')
t = mu('_t', 'teacher')
p = mu('_p', 'parent')
s = mu('_s', 'student')

# Link teacher user to a Teacher record
try:
    teacher_obj = Teacher.objects.first()
    if teacher_obj:
        UserProfile.objects.filter(user=t).update(teacher=teacher_obj)
except: pass

ALL_ADMIN = [
    '/school/', '/school/login/', '/school/profile/', '/school/settings/',
    '/school/users/', '/school/users/add/',
    '/school/students/', '/school/students/add/',
    '/school/teachers/', '/school/teachers/add/',
    '/school/classrooms/', '/school/classrooms/add/',
    '/school/subjects/', '/school/subjects/add/',
    '/school/attendance/', '/school/attendance/bulk/', '/school/attendance/add/',
    '/school/exams/', '/school/exams/add/',
    '/school/scores/', '/school/scores/add/',
    '/school/timetable/', '/school/timetable/add/',
    '/school/notifications/', '/school/notifications/add/',
    '/school/events/', '/school/events/add/',
    '/school/report-cards/', '/school/report-cards/add/',
    '/school/reports/students/', '/school/reports/teachers/',
    '/school/reports/attendance/', '/school/reports/scores/',
]

TEACHER_URLS = ['/school/', '/school/students/', '/school/attendance/', '/school/attendance/bulk/', '/school/exams/', '/school/scores/', '/school/timetable/', '/school/notifications/', '/school/report-cards/', '/school/profile/']
PARENT_URLS  = ['/school/', '/school/parent/attendance/', '/school/parent/results/', '/school/notifications/', '/school/events/', '/school/profile/']
STUDENT_URLS = ['/school/', '/school/student/attendance/', '/school/student/results/', '/school/timetable/', '/school/notifications/', '/school/profile/']

tests = [
    ('ADMIN',   admin, ALL_ADMIN),
    ('TEACHER', t,     TEACHER_URLS),
    ('PARENT',  p,     PARENT_URLS),
    ('STUDENT', s,     STUDENT_URLS),
]

errors = []
for role, user, urls in tests:
    c = Client(); c.force_login(user)
    print(f'\n── {role} ({len(urls)} pages) ──')
    for url in urls:
        try:
            r = c.get(url, SERVER_NAME='127.0.0.1')
            ok = r.status_code in (200, 302)
            print(f'  {"✓" if ok else "✗"} {r.status_code}  {url}')
            if not ok:
                # Get error detail
                if hasattr(r, 'context') and r.context:
                    errors.append(f'[{role}] {r.status_code} {url}')
                else:
                    errors.append(f'[{role}] {r.status_code} {url}')
        except Exception as e:
            tb = traceback.format_exc().split('\n')[-3]
            print(f'  ✗ EXC  {url}')
            print(f'         {tb.strip()}')
            errors.append(f'[{role}] EXC {url}: {str(e)[:80]}')

User.objects.filter(username__in=['_t','_p','_s']).delete()
print(f'\n{"="*55}')
if errors:
    print(f'❌  {len(errors)} ERROR(S):')
    for e in errors: print(f'   {e}')
else:
    total = sum(len(u) for _,_,u in tests)
    print(f'✅  ALL {total} PAGES PASS')
print('='*55)
