# ITSM Docker Settings

# If metrics enabled, see https://nofusscomputing.com/projects/centurion_erp/administration/monitoring/#django-exporter-setup)
# to configure the database metrics.
import os



API_TEST = True

AUTH_PASSWORD_VALIDATORS = []

CELERY_BROKER_URL = 'amqp://admin:admin@rabbitmq:5672/itsm'  # 'amqp://' is the connection protocol

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8003",
    "http://localhost:8003",
    "http://127.0.0.1",
]

CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

CSRF_COOKIE_SECURE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'itsm',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

if os.getenv('DJANGO_DEBUG') == 'False':

    DEBUG = False

else:

    DEBUG = True


FEATURE_FLAGGING_ENABLED = True    # Turn Feature Flagging on/off

FEATURE_FLAG_OVERRIDES = []    # Feature Flag Overrides. Takes preceedence over downloaded feature flags.

LOG_FILES = {    # Location where log files will be created
    "catch_all":"/var/log/catch-all.log",
    "centurion_trace": "/var/log/trace.log",
    "centurion": "/var/log/centurion.log",
    "error": "/var/log/error.log",
    "gunicorn": "/var/log/gunicorn.log",
    "rest_api": "/var/log/rest_api.log",
    "weblog": "/var/log/weblog.log",
}

METRICS_ENABLED = True

SECRET_KEY = 'django-insecure-b*41-$afq0yl)1e#qpz^-nbt-opvjwb#avv++b9rfdxa@b55sk'

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = False

SITE_URL = 'http://127.0.0.1:8003'

TRUSTED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://127.0.0.1:8003",
    "http://localhost:8003",
    "http://127.0.0.1",
]

USE_X_FORWARDED_HOST = True
