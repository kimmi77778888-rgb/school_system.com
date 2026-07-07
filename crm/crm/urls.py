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
from django.contrib.auth.decorators import login_required
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


@login_required
def debug_view(request):
    """Diagnostic view — staff only."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'forbidden'}, status=403)

    result = {}

    # School settings context processor
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

    # User profile access
    try:
        role = request.user.profile.role
        result['user_profile_role'] = role
    except Exception as e:
        result['user_profile_error'] = f"{type(e).__name__}: {e}"

    # DB counts
    try:
        from django.contrib.auth.models import User as _User
        from school.models import Student, Teacher, UserProfile
        result['db_users'] = _User.objects.count()
        result['db_profiles'] = UserProfile.objects.count()
        result['db_students'] = Student.objects.filter(is_active=True).count()
        result['db_teachers'] = Teacher.objects.filter(is_active=True).count()
        result['db_ok'] = True
    except Exception as e:
        result['db_ok'] = False
        result['db_error'] = str(e)

    # Cloudinary config status (no secrets exposed)
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
    api_key    = os.environ.get('CLOUDINARY_API_KEY', '')
    api_secret = os.environ.get('CLOUDINARY_API_SECRET', '')
    result['cloudinary_configured'] = bool(cloud_name and api_key and api_secret)
    result['media_backend'] = settings.STORAGES.get('default', {}).get('BACKEND', 'unknown')

    return JsonResponse(result, json_dumps_params={'indent': 2})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('debug/', debug_view, name='debug'),
    path('', lambda request: redirect('school:dashboard'), name='root'),
    path('school/', include('school.urls')),
]

# Serve media files locally (dev) and as fallback in production without Cloudinary.
# When CLOUDINARY_CLOUD_NAME is set, media URLs come directly from Cloudinary so
# this route is never hit — it is safe to always register it.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

