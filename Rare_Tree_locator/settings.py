"""
Django settings for Rare_Tree_locator project.
"""
import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-a97z%oub3*$jgymjk*3e15$tr%f=e@h)%*&45^^qoro%^4n)0s"
)

# SECURITY WARNING: don't run with debug turned on in production!
# Set DEBUG = True via Render environment variables if you need to debug further
DEBUG = os.environ.get("DEBUG", "False") == "True"
# DEBUG = True  # Set to True for development, change to False in production

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',

    # --- ADD CLOUDINARY HERE ---
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    # ---------------------------

    'MyApp.apps.MyappConfig',
    'TreeApp.apps.TreeappConfig',
    'BlogApp.apps.BlogappConfig',
    'DonationApp.apps.DonationappConfig',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves static files on Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Rare_Tree_locator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Rare_Tree_locator.wsgi.application'


# Database
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# SSLCOMMERZ Sandbox Credentials
SSLC_STORE_ID = 'raret68f48babe08eb'
SSLC_STORE_PASS = 'raret68f48babe08eb@ssl'
SSLC_MODE = 'sandbox'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'MyApp.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LOGIN_URL = 'login'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Modern WhiteNoise configuration (prevents 500 crashes on missing static assets)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

UNFOLD = {
    "SITE_HEADER": "Rare Tree Locator Admin",
    "SITE_TITLE": "Rare Tree Locator",
    "SITE_SYMBOL": "🌿",
    "SHOW_HISTORY": True,
    "THEME": "light",
}

# Cloudinary Credentials (uses Environment Variables in production)
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'u5s1vlhg'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '585634562132779'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'usG2uri3ERNfEbHBv2Wb6YxGZOA')
}

# Set Cloudinary as default storage for uploaded MEDIA files
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'