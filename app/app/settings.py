"""
Django settings for itsm project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import hashlib
import os
import sys

from pathlib import Path
from split_settings.tools import optional, include

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_DIR = '/etc/itsm'    # Primary Settings Directory


BUILD_REPO = os.getenv('CI_PROJECT_URL')
BUILD_SHA = os.getenv('CI_COMMIT_SHA')
BUILD_VERSION = os.getenv('CI_COMMIT_TAG')
DOCS_ROOT = 'https://nofusscomputing.com/projects/centurion_erp/user/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# Celery settings

CELERY_ACCEPT_CONTENT = ['json']
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True # broker_connection_retry_on_startup
CELERY_BROKER_URL = 'amqp://admin:admin@127.0.0.1:5672/itsm'

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#broker-use-ssl
# import ssl
# broker_use_ssl = {
#   'keyfile': '/var/ssl/private/worker-key.pem',
#   'certfile': '/var/ssl/amqp-server-cert.pem',
#   'ca_certs': '/var/ssl/myca.pem',
#   'cert_reqs': ssl.CERT_REQUIRED
# }

CELERY_BROKER_POOL_LIMIT = 3 # broker_pool_limit
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ENABLE_UTC = True

CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_TASK_SERIALIZER = 'json'

CELERY_TIMEZONE = 'UTC'
CELERY_TASK_DEFAULT_EXCHANGE = 'ITSM' # task_default_exchange
CELERY_TASK_DEFAULT_PRIORITY = 10 # 1-10=LOW-HIGH task_default_priority
# CELERY_TASK_DEFAULT_QUEUE = 'background'
CELERY_TASK_TIME_LIMIT = 3600 # task_time_limit
CELERY_TASK_TRACK_STARTED = True # task_track_started

# dont set concurrency for docer as it defaults to CPU count
CELERY_WORKER_CONCURRENCY = 2 # worker_concurrency -  Default: Number of CPU cores
CELERY_WORKER_DEDUPLICATE_SUCCESSFUL_TASKS = True # worker_deduplicate_successful_tasks
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1 # worker_max_tasks_per_child
# CELERY_WORKER_MAX_MEMORY_PER_CHILD = 10000 # 10000=10mb worker_max_memory_per_child - Default: No limit. Type: int (kilobytes)
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_WORKER_SEND_TASK_EVENTS = True # worker_send_task_events


# PROMETHEUS_METRICS_EXPORT_PORT_RANGE = range(8010, 8010)
# PROMETHEUS_METRICS_EXPORT_PORT = 8010
# PROMETHEUS_METRICS_EXPORT_ADDRESS = ''

METRICS_ENABLED = False                      # Enable Metrics
METRICS_EXPORT_PORT = 8080                   # Port to serve metrics on
METRICS_MULTIPROC_DIR = '/tmp/prometheus'    # path the metrics from multiple-process' save to

# django setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

#
# Defaults
#

ALLOWED_HOSTS = [ '*' ]          # Site host to serve
DEBUG = False                    # SECURITY WARNING: don't run with debug turned on in production!
SITE_URL = 'http://127.0.0.1'    # domain with HTTP method for the sites URL
SECRET_KEY = None                # You need to generate this
SESSION_COOKIE_AGE = 1209600     # Age the session cookie should live for in seconds. 
SSO_ENABLED = False              # Enable SSO
SSO_LOGIN_ONLY_BACKEND = None    # Use specified SSO backend as the ONLY method to login. (builting login form will not be used)
TRUSTED_ORIGINS = []             # list of trusted domains for CSRF



# Application definition
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 86400
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") # ToDo: https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# SECURE_SSL_REDIRECT = True    # Commented out so tests pass
# SECURE_SSL_HOST =        # ToDo: https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-host
SESSION_COOKIE_SECURE = True
# USE_X_FORWARDED_HOST = True # ToDo: https://docs.djangoproject.com/en/dev/ref/settings/#use-x-forwarded-host


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'corsheaders',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_json_api',
    'django_filters',
    'social_django',
    'django_celery_results',
    'core.apps.CoreConfig',
    'access.apps.AccessConfig',
    'itam.apps.ItamConfig',
    'itim.apps.ItimConfig',
    'assistance.apps.AssistanceConfig',
    'settings.apps.SettingsConfig',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'config_management.apps.ConfigManagementConfig',
    'project_management.apps.ProjectManagementConfig',
    'devops.apps.DevOpsConfig',
    'centurion_feature_flag',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'access.middleware.request.RequestTenancy',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.get_request.RequestMiddleware',
    'app.middleware.timezone.TimezoneMiddleware',
    # 'centurion_feature_flag.middleware.feature_flag.FeatureFlagMiddleware',
]


ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'app.context_processors.base.common',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = "http://127.0.0.1:3000"
LOGOUT_REDIRECT_URL = "login"

LOGIN_URL = '/account/login'
LOGIN_REQUIRED = True

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    BASE_DIR / "project-static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_TITLE = "Centurion ERP"


API_ENABLED = True

if API_ENABLED:

    INSTALLED_APPS += [
    'api.apps.ApiConfig',
]

    REST_FRAMEWORK = {
        'PAGE_SIZE': 10,
        'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticated',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'api.auth.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PAGINATION_CLASS':
            'rest_framework_json_api.pagination.JsonApiPageNumberPagination',
        # leaving these uncommented, even though are the default renderers
        # causes the api to require inputs the fields under an 'attributes' key
        # 'DEFAULT_PARSER_CLASSES': (
        #     'rest_framework_json_api.parsers.JSONParser',
        #     'rest_framework.parsers.FormParser',
        #     'rest_framework.parsers.MultiPartParser'
        # ),
        # leaving these uncommented, even though are the default renderers
        # causes the api to output the fields under a 'attributes' key
        # 'DEFAULT_RENDERER_CLASSES': (
        #     'rest_framework_json_api.renderers.JSONRenderer',
        #     'rest_framework_json_api.renderers.BrowsableAPIRenderer',
        # ),
        'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
        'DEFAULT_FILTER_BACKENDS': (
            # 'rest_framework_json_api.filters.QueryParameterValidationFilter',
            'rest_framework.filters.SearchFilter',
            'rest_framework_json_api.django_filters.DjangoFilterBackend',
            'rest_framework_json_api.filters.OrderingFilter',
        ),
        # 'SEARCH_PARAM': 'filter[search]',
        # 'TEST_REQUEST_RENDERER_CLASSES': (
        #     'rest_framework_json_api.renderers.JSONRenderer',
        # ),
        # 'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
        'DEFAULT_VERSION': 'v1',
        'ALLOWED_VERSIONS': [
            'v1',
            'v2'
        ]
    }

    SPECTACULAR_SETTINGS = {
        'TITLE': 'Centurion ERP API',
        'DESCRIPTION': """This UI exists to server the purpose of being the API documentation.

Centurion ERP's API is versioned, with [v1 Depreciated](/api/swagger) and [v2 as the current](/api/v2/docs).

For CRUD actions `Add`, `update` and `replace` the serializer that returns is the Models `View` serializer.

**Note:** _API v2 is currently in beta phase. AS such is subject to change. When the new UI ius released, API v2 will move to stable._

## Authentication

Access to the API is restricted and requires authentication. Available authentication methods are:

- Session
- Token

Session authentication is made available after logging into the application via the login interface.

Token authentication is via an API token that a user will generate within their 
[settings panel](https://nofusscomputing.com/projects/django-template/user/user_settings/#api-tokens).

## Examples

curl:
- Simple API Request: `curl -X GET <url>/api/ -H 'Authorization: Token <token>'`

- Post an Inventory File:

    ``` bash
    curl --header "Content-Type: application/json" \\
    --header "Authorization: Token <token>" \\
    --request POST \\
    --data @<path to inventory file>/<file name>.json \\
    <url>/api/device/inventory
    ```

        """,
        'VERSION': '',
        'SCHEMA_PATH_PREFIX': '/api/v2/|/api/',
        'SERVE_INCLUDE_SCHEMA': False,
        'SWAGGER_UI_DIST': 'SIDECAR',
        'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
        "SWAGGER_UI_SETTINGS": '''{
            filter: true,
            defaultModelsExpandDepth: -1,
            deepLinking: true,
        }''',
        'REDOC_DIST': 'SIDECAR',
        'PREPROCESSING_HOOKS': [
            'drf_spectacular.hooks.preprocess_exclude_path_format'
        ],
    }

DATETIME_FORMAT = 'j N Y H:i:s'
#
# Settings for unit tests
#

RUNNING_TESTS = 'test' in str(sys.argv)

if RUNNING_TESTS:
    SECRET_KEY = 'django-insecure-tests_are_being_run'

#
# Load user settings files
#
if os.path.isdir(SETTINGS_DIR):

    settings_files = os.path.join(SETTINGS_DIR, '*.py')
    include(optional(settings_files))

#
# Settings to reset to prevent user from over-riding
#
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

CSRF_TRUSTED_ORIGINS = [
    SITE_URL,
    *TRUSTED_ORIGINS
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    INTERNAL_IPS = [
        "127.0.0.1",
    ]


if METRICS_ENABLED:

    INSTALLED_APPS += [ 'django_prometheus', ]

    MIDDLEWARE = [ 
        'django_prometheus.middleware.PrometheusBeforeMiddleware' 
    ] + MIDDLEWARE + [
        'django_prometheus.middleware.PrometheusAfterMiddleware',
    ]

    if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':

        DATABASES['default']['ENGINE'] = 'django_prometheus.db.backends.sqlite3',


if SSO_ENABLED:

    if SSO_LOGIN_ONLY_BACKEND:
        LOGIN_URL = f'/sso/login/{SSO_LOGIN_ONLY_BACKEND}/'

    AUTHENTICATION_BACKENDS += (
        *SSO_BACKENDS,
    )

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.social_auth.associate_by_email',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )


if BUILD_VERSION:

    feature_flag_version = str(BUILD_VERSION) + '+' + str(BUILD_SHA)[8:]

else:

    feature_flag_version = str(BUILD_SHA)


""" Unique ID Rational

Unique ID generation required to determine how many installations are deployed. Also provides the opportunity
should it be required in the future to enable feature flags on a per `unique_id`.

Objects:

- CELERY_BROKER_URL
- SITE_URL
- SECRET_KEY

Will provide enough information alone once hashed, to identify a majority of deployments as unique.

Adding object `feature_flag_version`, Ensures that as each release occurs that a deployments `unique_id` will
change, thus preventing long term monitoring of a deployments usage of Centurion.

value `DOCS_ROOT` is added so there is more data to hash.

You are advised not to change the `unique_id` as you may inadvertantly reduce your privacy. However the choice
is yours. If you do change the value ensure that it's still hashed as a sha256 hash.
"""
unique_id = str(f'{CELERY_BROKER_URL}{DOCS_ROOT}{SITE_URL}{SECRET_KEY}{feature_flag_version}')
unique_id = hashlib.sha256(unique_id.encode()).hexdigest()
