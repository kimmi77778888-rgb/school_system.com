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
import sys, os

def health_check(request):
    """Diagnostic endpoint — shows what's working on Render."""
    info = {
        'status': 'ok',
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
    except Exception as e:
        info['db_ok'] = False
        info['db_error'] = str(e)
    try:
        from school.models import SchoolSettings
        SchoolSettings.get()
        info['school_settings_ok'] = True
    except Exception as e:
        info['school_settings_ok'] = False
        info['school_settings_error'] = str(e)
    return JsonResponse(info)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health'),
    path('', lambda request: redirect('school:dashboard'), name='root'),
    path('school/', include('school.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

