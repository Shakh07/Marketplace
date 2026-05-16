"""
Django settings for ecommerce project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-ecommerce-dev-key-change-in-production')

DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    # Third party
    'rest_framework',
    'corsheaders',
    # Local apps
    'apps.accounts',
    'apps.catalog',
    'apps.orders',
    'apps.reviews',
    'apps.warehouse',
    'apps.suppliers',
    'apps.returns',
    'apps.manager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files in production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.accounts.context_processors.site_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

import dj_database_url
import os

# Database — Docker: DATABASE_URL env var. Local: individual DB_* vars or DATABASE_URL
_db_url = os.environ.get('DATABASE_URL', '')

if _db_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=_db_url,
            conn_max_age=600,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME':     os.environ.get('DB_NAME', 'nexus_db'),
            'USER':     os.environ.get('DB_USER', 'nexus_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'nexus_password'),
            'HOST':     os.environ.get('DB_HOST', 'localhost'),
            'PORT':     os.environ.get('DB_PORT', '5432'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '
NUMBER_GROUPING = 3

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
# WhiteNoise: gzip compress + cache-busting filenames
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# CORS — production'da aniq domenlar ko'rsatiladi
_cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if _cors_origins:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in _cors_origins.split(',')]
else:
    CORS_ALLOW_ALL_ORIGINS = True  # Faqat local dev uchun

# Security headers
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = False   # JS dan o'qish uchun
CSRF_COOKIE_SAMESITE = 'Lax'

# HTTPS — Production'da faollashadi (DEBUG=False bo'lganda)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000        # 1 yil
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# Login/Logout redirects
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Unfold Admin Panel Configuration
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "NEXUS Admin",
    "SITE_HEADER": "NEXUS",
    "SITE_SYMBOL": "speed", # Material symbol
    "DASHBOARD_CALLBACK": "ecommerce.dashboard.dashboard_callback",
    
    "COLORS": {
        "primary": {
            "50": "235 245 255",
            "100": "204 229 255",
            "200": "153 204 255",
            "300": "102 178 255",
            "400": "51 153 255",
            "500": "0 108 225", # NEXUS Blue
            "600": "0 86 180",
            "700": "0 65 135",
            "800": "0 43 90",
            "900": "0 22 45",
            "950": "0 11 22",
        },
    },

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("BOSHQARUV"),
                "separator": True,
                "items": [
                    {
                        "title": _("Statistika"),
                        "icon": "dashboard",
                        "link": "/admin/",
                    },
                ],
            },
            {
                "title": _("KATALOG"),
                "separator": True,
                "items": [
                    {
                        "title": _("Kategoriyalar"),
                        "icon": "category",
                        "link": "/admin/catalog/category/",
                    },
                    {
                        "title": _("Brendlar"),
                        "icon": "verified",
                        "link": "/admin/catalog/brand/",
                    },
                    {
                        "title": _("Mahsulotlar"),
                        "icon": "inventory_2",
                        "link": "/admin/catalog/product/",
                    },
                ],
            },
            {
                "title": _("SOTUVLAR"),
                "separator": True,
                "items": [
                    {
                        "title": _("Barcha Buyurtmalar"),
                        "icon": "shopping_bag",
                        "link": "/admin/orders/order/",
                    },
                    {
                        "title": _("Tranzaksiyalar"),
                        "icon": "account_balance_wallet",
                        "link": "/admin/orders/paymenttransaction/",
                    },
                ],
            },
            {
                "title": _("FOYDALANUVCHILAR"),
                "separator": True,
                "items": [
                    {
                        "title": _("Mijozlar"),
                        "icon": "group",
                        "link": "/admin/accounts/customuser/",
                    },
                    {
                        "title": _("Sharhlar"),
                        "icon": "reviews",
                        "link": "/admin/reviews/review/",
                    },
                ],
            },
            {
                "title": _("SOZLAMALAR"),
                "separator": True,
                "items": [
                    {
                        "title": _("Sayt Sozlamalari"),
                        "icon": "settings",
                        "link": "/admin/accounts/sitesettings/",
                    },
                ],
            },
        ],
    },
}
