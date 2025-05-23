# ITSM Docker Settings

# If metrics enabled, see https://nofusscomputing.com/projects/centurion_erp/administration/monitoring/#django-exporter-setup)
# to configure the database metrics.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3',
    }
}

#
# Example MariaDB/MySQL setup
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'itsm',
#         'USER': '<db username>',
#         'PASSWORD': '<db password>',
#         'HOST': '<db host/ip address>',
#         'PORT': '',
#     }
# }

#
#
#
# CELERY_BROKER_URL = 'amqp://<username>:<password>@<host>:<port>/[<message host>]'  # 'amqp://' is the connection protocol

FEATURE_FLAGGING_ENABLED = True    # Turn Feature Flagging on/off

FEATURE_FLAG_OVERRIDES = []    # Feature Flag Overrides. Takes preceedence over downloaded feature flags.


LOG_FILES = {    # Location where log files will be created
    "centurion": "/var/log/centurion.log",
    "weblog": "/var/log/weblog.log",
    "rest_api": "/var/log/rest_api.log",
    "catch_all":"/var/log/catch-all.log"
}


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True
