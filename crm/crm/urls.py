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
    result['cloudinary_cloud_name'] = cloud_name if cloud_name else None
    result['media_backend'] = settings.STORAGES.get('default', {}).get('BACKEND', 'unknown')
    
    # Test cloudinary connection
    if cloud_name:
        try:
            import cloudinary
            # Try to ping cloudinary
            test_result = cloudinary.api.ping()
            result['cloudinary_ping'] = 'ok'
        except Exception as e:
            result['cloudinary_ping'] = f'ERROR: {type(e).__name__}: {e}'

    return JsonResponse(result, json_dumps_params={'indent': 2})


@login_required
def test_upload(request):
    """Test image upload endpoint."""
    if not request.user.is_staff:
        return JsonResponse({'error': 'forbidden'}, status=403)
    
    result = {'method': request.method}
    
    # Show config status
    import os, cloudinary
    cfg = cloudinary.config()
    result['cloudinary_cloud_name'] = cfg.cloud_name or None
    result['cloudinary_api_key_set'] = bool(cfg.api_key)
    result['env_vars'] = {
        'CLOUDINARY_CLOUD_NAME': bool(os.environ.get('CLOUDINARY_CLOUD_NAME')),
        'CLOUDINARY_API_KEY': bool(os.environ.get('CLOUDINARY_API_KEY')),
        'CLOUDINARY_API_SECRET': bool(os.environ.get('CLOUDINARY_API_SECRET')),
    }
    
    # Test ping
    try:
        ping_result = cloudinary.api.ping()
        result['cloudinary_ping'] = ping_result
    except Exception as e:
        result['cloudinary_ping_error'] = f'{type(e).__name__}: {str(e)}'
    
    if request.method == 'POST' and request.FILES.get('test_file'):
        try:
            from django.core.files.storage import default_storage
            file = request.FILES['test_file']
            
            # Save to storage backend
            path = default_storage.save(f'test/{file.name}', file)
            url = default_storage.url(path)
            
            result['upload'] = {
                'status': 'success',
                'path': path,
                'url': url,
                'backend': settings.STORAGES.get('default', {}).get('BACKEND', 'unknown'),
            }
        except Exception as e:
            result['upload'] = {
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc(),
            }
        
        return JsonResponse(result, json_dumps_params={'indent': 2})
    
    # GET: show form with diagnostic info
    from django.http import HttpResponse
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Upload</title>
        <style>
            body {{ font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 20px; }}
            h2 {{ color: #2563eb; }}
            .status {{ background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 16px; margin: 16px 0; }}
            .ok {{ background: #dcfce7; border-color: #86efac; }}
            .error {{ background: #fee2e2; border-color: #fca5a5; }}
            pre {{ background: #f1f5f9; padding: 12px; border-radius: 6px; overflow-x: auto; }}
            button {{ background: #2563eb; color: white; border: none; padding: 10px 20px; border-radius: 6px; cursor: pointer; }}
            button:hover {{ background: #1d4ed8; }}
        </style>
    </head>
    <body>
        <h2>🧪 Test Image Upload</h2>
        
        <div class="status {('ok' if result.get('cloudinary_ping') else 'error')}">
            <strong>Cloudinary Status:</strong><br>
            <pre>{repr(result)}</pre>
        </div>
        
        <form method="post" enctype="multipart/form-data">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <input type="file" name="test_file" accept="image/*" required style="margin: 10px 0;">
            <button type="submit">📤 Upload Test Image</button>
        </form>
        
        <hr style="margin: 30px 0;">
        <a href="/debug/">← Back to Debug Info</a> | 
        <a href="/school/">← Back to Dashboard</a>
    </body>
    </html>
    '''
    return HttpResponse(html)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('debug/', debug_view, name='debug'),
    path('test-upload/', test_upload, name='test_upload'),
    path('', lambda request: redirect('school:dashboard'), name='root'),
    path('school/', include('school.urls')),
]

# Serve media files locally (dev) and as fallback in production without Cloudinary.
# When CLOUDINARY_CLOUD_NAME is set, media URLs come directly from Cloudinary so
# this route is never hit — it is safe to always register it.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

