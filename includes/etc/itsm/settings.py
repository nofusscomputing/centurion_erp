# ITSM Docker Settings


# ADDITIONAL_APPS: list = []    # Any additional Django apps to install

CSRF_COOKIE_PATH = '/'                # If hosting on a different path, this must be updated to match.

#
# Note: If using SSO, the cookie age here must be set to a few seconds less than the SSO providers
#       cookie / token (refresh) expiry. This allows for Centurion ERP to force reauthentication.
#
SESSION_COOKIE_AGE = ( 3600 * 4 )     # 4 hours. Age the session cookie should live for in seconds.
SESSION_COOKIE_DOMAIN = None          # This must be set to the domain that Centurion ERP is hosted on.
SESSION_COOKIE_PATH = '/'             # If hosting on a different path, this must be updated to match.

#
# Note: This cookie age should be slightly longer than the session cookie age. This allows for the
#       session cookie to expire and ensures that the CSRF cookie is always valid for the session
#       duration.
#
CSRF_COOKIE_AGE = ( SESSION_COOKIE_AGE + 2 )     # Age the CSRF cookie should live for in seconds.


#
# If metrics enabled, see https://nofusscomputing.com/projects/centurion_erp/administration/monitoring/#django-exporter-setup)
# to configure the database metrics.
#
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
    "catch_all":"/var/log/catch-all.log",
    "centurion_trace": "/var/log/trace.log",
    "centurion": "/var/log/centurion.log",
    "error": "/var/log/error.log",
    "rest_api": "/var/log/rest_api.log",
    "weblog": "/var/log/weblog.log",
}


SECRET_KEY = None    # You must generate this

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

SITE_URL = 'http://127.0.0.1'    # Base URL the site is hosted on.

# TRACE_LOGGING = True                                                                # Enable Trace Logging.
# CENTURION_LOGGING['loggers']['centurion.trace']['level'] = CenturionLogger.TRACE    # Set Trace Logging level. normally not required

USE_X_FORWARDED_HOST = True
