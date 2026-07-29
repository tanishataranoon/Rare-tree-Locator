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
    'cloudinary_storage',
    'django.contrib.staticfiles',
    'cloudinary',
    'import_export',

    # Project Apps
    'MyApp.apps.MyappConfig',
    'TreeApp.apps.TreeappConfig',
    'BlogApp.apps.BlogappConfig',
    'DonationApp.apps.DonationappConfig',
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


# Static Files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Prevents WhiteNoise manifest crashes on missing assets
WHITENOISE_MANIFEST_STRICT = False

# Disable compression processing for unfold/admin vendor files if using compressed storage
WHITENOISE_SKIP_COMPRESS_EXTENSIONS = (
    'jpg', 'jpeg', 'png', 'gif', 'webp', 'zip', 'gz', 'tgz', 'bz2', 'tbz',
    'woff', 'woff2', 'eot', 'ttf', 'otf', 'svg', 'LICENSE', 'md', 'txt'
)


# Cloudinary Media Storage Configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', 'u5s1vlhg'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', '585634562132779'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', 'usG2uri3ERNfEbHBv2Wb6YxGZOA'),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Storage Backends Configuration (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        # Standard WhiteNoise storage prevents multi-threaded compression race conditions
        "BACKEND": "whitenoise.storage.StaticFilesStorage",
    },
}

# Legacy fallback compatibility required by django-cloudinary-storage
STATICFILES_STORAGE = "whitenoise.storage.StaticFilesStorage"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


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