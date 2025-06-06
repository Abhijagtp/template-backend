import environ
import os
import dj_database_url
from pathlib import Path
import cloudinary  # Add this import
import logging

# Define BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-fallback-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DJANGO_DEBUG', default=False)

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'templates',
    'rest_framework',
    'corsheaders',
    'cloudinary',  # Ensure this is before cloudinary_storage
    'cloudinary_storage',  # Ensure this order
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Disabled as in your original
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL', default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')),
        conn_max_age=600
    )
}

# Password validation
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

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://yourtemplatehub.com',
    'https://www.yourtemplatehub.com',
    'http://localhost:5173',
    'https://template-frontend-2zle.onrender.com',
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='support@yourtemplatehub.com')
FRONTEND_URL = env('FRONTEND_URL', default='https://yourtemplatehub.com')

# Cashfree settings
CASHFREE_APP_ID = env('CASHFREE_APP_ID')
CASHFREE_SECRET_KEY = env('CASHFREE_SECRET_KEY')
CASHFREE_ENV = env('CASHFREE_ENV', default='sandbox')

# Debug Cashfree settings
print("CASHFREE_ENV (raw):", repr(CASHFREE_ENV))
print("CASHFREE_ENV (length):", len(CASHFREE_ENV))
print("CASHFREE_ENV (lowercase):", CASHFREE_ENV.lower())
if CASHFREE_ENV.lower().strip() == 'sandbox':
    CASHFREE_BASE_URL = 'https://sandbox.cashfree.com'
    print("Setting CASHFREE_BASE_URL to sandbox")
else:
    CASHFREE_BASE_URL = 'https://api.cashfree.com'
    print("Setting CASHFREE_BASE_URL to production")
print("CASHFREE_APP_ID:", CASHFREE_APP_ID)
print("CASHFREE_SECRET_KEY:", CASHFREE_SECRET_KEY)
print("CASHFREE_ENV:", CASHFREE_ENV)
print("CASHFREE_BASE_URL:", CASHFREE_BASE_URL)



# Set up logging
logger = logging.getLogger(__name__)
# Cloudinary settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

# Validate and initialize Cloudinary SDK
try:
    if not all(CLOUDINARY_STORAGE.values()):
        missing_vars = [key for key, value in CLOUDINARY_STORAGE.items() if not value]
        logger.error(f"Missing Cloudinary environment variables: {missing_vars}")
        raise Exception(f"Missing Cloudinary environment variables: {missing_vars}")

    cloudinary.config(
        cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=CLOUDINARY_STORAGE['API_KEY'],
        api_secret=CLOUDINARY_STORAGE['API_SECRET'],
        secure=True
    )
    logger.info("Cloudinary SDK initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Cloudinary SDK: {str(e)}")
    raise Exception(f"Failed to initialize Cloudinary SDK: {str(e)}")

# Optionally, define these for easier access in code
CLOUDINARY_CLOUD_NAME = CLOUDINARY_STORAGE['CLOUD_NAME']
CLOUDINARY_API_KEY = CLOUDINARY_STORAGE['API_KEY']
CLOUDINARY_API_SECRET = CLOUDINARY_STORAGE['API_SECRET']

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



print("CLOUDINARY_CLOUD_NAME:", os.getenv('CLOUDINARY_CLOUD_NAME'))
print("CLOUDINARY_API_KEY:", os.getenv('CLOUDINARY_API_KEY'))
print("CLOUDINARY_API_SECRET:", os.getenv('CLOUDINARY_API_SECRET'))
print("DEFAULT_FILE_STORAGE:", DEFAULT_FILE_STORAGE)