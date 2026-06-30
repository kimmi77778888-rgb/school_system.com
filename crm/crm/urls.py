"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import JsonResponse
import sys, os, traceback

def health_check(request):
    """Diagnostic endpoint."""
    info = {
        'status': 'ok',
        'commit': '6e3a78e',
        'python': sys.version,
        'django': __import__('django').get_version(),
        'debug': settings.DEBUG,
        'database': 'postgresql' if os.environ.get('DATABASE_URL') else 'sqlite',
        'staticfiles_backend': settings.STORAGES.get('staticfiles', {}).get('BACKEND', 'unknown'),
        'cloudinary': bool(os.environ.get('CLOUDINARY_CLOUD_NAME')),
        'allowed_hosts': settings.ALLOWED_HOSTS,
    }
    try:
        from django.contrib.auth.models import User
        info['db_users'] = User.objects.count()
        info['db_ok'] = True
        users_without_profile = []
        for u in User.objects.all():
            try:
                _ = u.profile
            except Exception:
                users_without_profile.append(u.username)
        info['users_without_profile'] = users_without_profile
    except Exception as e:
        info['db_ok'] = False
        info['db_error'] = str(e)
    try:
        from school.models import SchoolSettings, UserProfile
        SchoolSettings.get()
        info['school_settings_ok'] = True
        info['total_profiles'] = UserProfile.objects.count()
    except Exception as e:
        info['school_settings_ok'] = False
        info['school_settings_error'] = str(e)
    return JsonResponse(info)


def debug_view(request):
    """Try to simulate the failing page and capture the exact error."""
    result = {}
    # Test 1: school settings context processor
    try:
        from school.context_processors import school_settings
        ctx = school_settings(request)
        result['school_settings_cp'] = 'ok'
        school = ctx.get('school')
        result['school_name'] = str(school.school_name) if school else None
        if school and school.logo:
            try:
                result['logo_url'] = school.logo.url
            except Exception as e:
                result['logo_url_error'] = f"{type(e).__name__}: {e}"
    except Exception as e:
        result['school_settings_cp'] = f"ERROR: {traceback.format_exc()}"

    # Test 2: user profile access
    if request.user.is_authenticated:
        try:
            role = request.user.profile.role
            result['user_profile_role'] = role
        except Exception as e:
            result['user_profile_error'] = f"{type(e).__name__}: {e}"

    # Test 3: user list query
    try:
        from django.contrib.auth.models import User
        users = list(User.objects.select_related('profile').order_by('username'))
        result['user_list_count'] = len(users)
        for u in users:
            try:
                p = u.profile
                if p.photo and p.photo.name:
                    try:
                        _ = p.photo.url
                    except Exception as e:
                        result[f'user_{u.username}_photo_error'] = f"{type(e).__name__}: {e}"
            except Exception as e:
                result[f'user_{u.username}_profile_error'] = f"{type(e).__name__}: {e}"
    except Exception as e:
        result['user_list_error'] = f"{type(e).__name__}: {e}"

    # Test 4: student list query
    try:
        from school.models import Student
        students = list(Student.objects.filter(is_active=True).select_related('classroom__grade')[:5])
        result['student_list_count'] = len(students)
    except Exception as e:
        result['student_list_error'] = f"{type(e).__name__}: {traceback.format_exc()}"

    # Test 5: teacher list query
    try:
        from school.models import Teacher
        teachers = list(Teacher.objects.filter(is_active=True)[:5])
        result['teacher_list_count'] = len(teachers)
    except Exception as e:
        result['teacher_list_error'] = f"{type(e).__name__}: {traceback.format_exc()}"

    # Test Cloudinary configuration
    try:
        import cloudinary
        import cloudinary.uploader
        cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
        api_key = os.environ.get('CLOUDINARY_API_KEY', '')
        api_secret = os.environ.get('CLOUDINARY_API_SECRET', '')
        result['cloudinary_cloud_name'] = cloud_name[:4] + '***' if cloud_name else 'NOT SET'
        result['cloudinary_api_key'] = api_key[:4] + '***' if api_key else 'NOT SET'
        result['cloudinary_api_secret_set'] = bool(api_secret)
        result['cloudinary_configured'] = bool(cloud_name and api_key and api_secret)
        # Check DEFAULT_FILE_STORAGE backend
        result['media_backend'] = settings.STORAGES.get('default', {}).get('BACKEND', 'unknown')
    except Exception as e:
        result['cloudinary_error'] = str(e)
    from django.template.loader import render_to_string
    from django.contrib.auth.models import User
    from school.models import Student, Teacher

    for tpl, ctx_fn in [
        ('school/users/user_list.html', lambda: {'users': User.objects.select_related('profile').order_by('username')}),
        ('school/student_list.html',    lambda: {'students': Student.objects.filter(is_active=True).select_related('classroom__grade'), 'q': '', 'classrooms': [], 'selected_classroom': '', 'role': 'admin'}),
        ('school/teacher_list.html',    lambda: {'teachers': Teacher.objects.filter(is_active=True), 'q': '', 'role': 'admin'}),
        ('school/auth/profile.html',    lambda: {'form': __import__('school.forms', fromlist=['ProfileUpdateForm']).ProfileUpdateForm(user=request.user), 'profile': request.user.profile}),
    ]:
        try:
            from django.template import RequestContext
            render_to_string(tpl, ctx_fn(), request=request)
            result[f'render_{tpl}'] = 'ok'
        except Exception as e:
            result[f'render_{tpl}_ERROR'] = traceback.format_exc()

    return JsonResponse(result, json_dumps_params={'indent': 2})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('debug/', debug_view, name='debug'),
    path('', lambda request: redirect('school:dashboard'), name='root'),
    path('school/', include('school.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

