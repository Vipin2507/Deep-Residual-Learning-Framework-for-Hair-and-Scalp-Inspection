"""
Production settings for deployment on Render
"""
from .settings import *
import os

# MongoDB configuration
MONGODB_URI = os.environ.get('MONGODB_URI')
MONGODB_NAME = os.environ.get('MONGODB_NAME', 'hairscalp_db')

# SECURITY SETTINGS
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-q$p7bwhr1&oiimk3@r59_5-nwsyqhqr*$wf+7pq=ko4+q(71m0')

# ALLOWED HOSTS
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.railway.app',  # Railway domains
    '.onrender.com',  # Render domains (if still using)
    '.vercel.app',    # Vercel frontend domain (if needed)
]

# CORS SETTINGS for Vercel frontend
CORS_ALLOWED_ORIGINS = [
    "https://your-app.vercel.app",  # Replace with your actual Vercel domain
    "http://localhost:3000",
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF SETTINGS
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',  # Railway domains
    'https://*.onrender.com',  # Render domains (if still using)
    'https://*.vercel.app',
]

# DATABASE
# MongoDB Atlas configuration using pymongo directly
if MONGODB_URI:
    from pymongo import MongoClient
    # Store connection for use in models
    MONGODB_CLIENT = MongoClient(MONGODB_URI)
    MONGODB_DATABASE = MONGODB_CLIENT[MONGODB_NAME]
    
    # Still need to define DATABASES for Django auth/sessions
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    # Fallback to SQLite if MongoDB not configured
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# STATIC FILES
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Only include static dirs that exist
import os as _os
_static_dir = _os.path.join(BASE_DIR, 'myapp', 'static')
if _os.path.exists(_static_dir):
    STATICFILES_DIRS = [_static_dir]
else:
    STATICFILES_DIRS = []

# WhiteNoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MEDIA FILES
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ML MODEL PATH - Point to the model in the parent directory
ML_MODEL_PATH = os.path.join(BASE_DIR.parent, 'best_model.pth')

# SECURITY
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
