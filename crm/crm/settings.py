from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-xh0+*f#rw+je!r5@@06agyl0#=!8-v*m5oq5gdjh3oo*dg6mr%')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']  # Render handles host validation via its proxy

# ──────────────────────────────────────────────────────
#  JAZZMIN — Modern Admin UI
# ──────────────────────────────────────────────────────
JAZZMIN_SETTINGS = {
    "site_title": "BELTEI School",
    "site_header": "BELTEI International University",
    "site_brand": "School MS",
    "welcome_sign": "Welcome to BELTEI School Management",
    "copyright": "BELTEI International University",
    "topmenu_links": [
        {"name": "School Dashboard", "url": "/school/", "new_window": False},
        {"name": "Home", "url": "admin:index"},
    ],
    "hide_apps": ["auth"],
    "icons": {
        "school.student":      "fas fa-user-graduate",
        "school.teacher":      "fas fa-chalkboard-teacher",
        "school.classroom":    "fas fa-school",
        "school.subject":      "fas fa-book",
        "school.attendance":   "fas fa-calendar-check",
        "school.score":        "fas fa-chart-bar",
        "school.grade":        "fas fa-layer-group",
        "school.academicyear": "fas fa-calendar-alt",
        "school.examtype":     "fas fa-file-alt",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "show_sidebar": True,
    "navigation_expanded": True,
    "changeform_format": "horizontal_tabs",
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}

# ──────────────────────────────────────────────────────
#  INSTALLED APPS  — jazzmin must be BEFORE admin
# ──────────────────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary',
    'accounts',
    'school',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'school' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'school.context_processors.school_settings',
                'school.context_processors.ensure_user_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'crm.wsgi.application'

# ──────────────────────────────────────────────────────
#  DATABASE
# ──────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Phnom_Penh'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────
#  STATIC FILES — whitenoise serves them, no manifest needed
# ──────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ──────────────────────────────────────────────────────
#  CLOUDINARY — supports both CLOUDINARY_URL and individual vars
# ──────────────────────────────────────────────────────
import cloudinary

_CLOUDINARY_URL        = os.environ.get('CLOUDINARY_URL', '')
_CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME', '')
_CLOUDINARY_API_KEY    = os.environ.get('CLOUDINARY_API_KEY', '')
_CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET', '')

if _CLOUDINARY_URL:
    # cloudinary://api_key:api_secret@cloud_name  — SDK parses this automatically
    cloudinary.config(cloudinary_url=_CLOUDINARY_URL, secure=True)
    _CLOUDINARY_CONFIGURED = True
elif _CLOUDINARY_CLOUD_NAME:
    cloudinary.config(
        cloud_name=_CLOUDINARY_CLOUD_NAME,
        api_key=_CLOUDINARY_API_KEY,
        api_secret=_CLOUDINARY_API_SECRET,
        secure=True,
    )
    _CLOUDINARY_CONFIGURED = True
else:
    _CLOUDINARY_CONFIGURED = False

STORAGES = {
    "default": {
        "BACKEND": (
            "crm.cloudinary_storage.MediaCloudinaryStorage"
            if _CLOUDINARY_CONFIGURED
            else "django.core.files.storage.FileSystemStorage"
        ),
    },
    "staticfiles": {
        # Simple compressed storage — no manifest.json required
        # Works even after Render container restarts (no persistent disk)
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL           = '/school/login/'
LOGIN_REDIRECT_URL  = '/school/'
LOGOUT_REDIRECT_URL = '/school/login/'

# ──────────────────────────────────────────────────────
#  LOGGING — errors visible in Render log panel
# ──────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'crm.cloudinary_storage': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
