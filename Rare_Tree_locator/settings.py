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
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")

# # NEW: Default to True for local development when env var is not set
# DEBUG = os.environ.get("DEBUG", "True").lower() in ("true", "1", "t")

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # Unfold Admin (Must precede django.contrib.admin)
    'unfold',
    'unfold.contrib.import_export',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # Third-party Storage & Tools
    'django.contrib.staticfiles',
    'storages',  # Required for Supabase S3 integration
    'import_export',

    # Project Apps
    'MyApp.apps.MyappConfig',
    'TreeApp.apps.TreeappConfig',
    'BlogApp.apps.BlogappConfig',
    'DonationApp.apps.DonationappConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves CSS/JS on Render
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


# Database Configuration
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}


# Custom User Model & Authentication
AUTH_USER_MODEL = 'MyApp.User'

LOGIN_URL = 'login'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static Files (CSS, JavaScript)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Prevents WhiteNoise from crashing on missing vendor assets (e.g., Unfold)
WHITENOISE_MANIFEST_STRICT = False


# Supabase Storage (S3 Protocol) Configuration
# Supabase Storage (S3 Protocol) Configuration
SUPABASE_PROJECT_ID = os.environ.get('SUPABASE_PROJECT_ID', 'vndlpftgnsrnnslzwfcb')

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'fb87820540f85e04ca81ba05d7ce3141')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '53862ea251df04cee488fc892a570966c090cdf6f872a72abd0e87e3aef5e3bb')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'media')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ap-south-1')

# Correct variable reference inside the f-string:
AWS_S3_ENDPOINT_URL = f"https://{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/s3"
AWS_S3_CUSTOM_DOMAIN = f"{SUPABASE_PROJECT_ID}.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}"

AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False  # Public URLs for images


# Storage Configuration (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Legacy Compatibility Backends
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/" if SUPABASE_PROJECT_ID else '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# SSLCOMMERZ Credentials
SSLC_STORE_ID = os.environ.get('SSLC_STORE_ID', 'raret68f48babe08eb')
SSLC_STORE_PASS = os.environ.get('SSLC_STORE_PASS', 'raret68f48babe08eb@ssl')
SSLC_MODE = os.environ.get('SSLC_MODE', 'sandbox')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Unfold Admin Theme Configuration
UNFOLD = {
    "SITE_HEADER": "Rare Tree Locator Admin",
    "SITE_TITLE": "Rare Tree Locator",
    "SITE_SYMBOL": "🌿",
    "SHOW_HISTORY": True,
    "THEME": "light",
}