"""
Django settings for itsm project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

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
DOCS_ROOT = 'https://nofusscomputing.com/projects/django-template/user/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


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
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS =    # ToDo: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECURE_HSTS_SECONDS
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") # ToDo: https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# SECURE_SSL_REDIRECT = True
# SECURE_SSL_HOST =        # ToDo: https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-host
# SESSION_COOKIE_SECURE = True
# USE_X_FORWARDED_HOST = True # ToDo: https://docs.djangoproject.com/en/dev/ref/settings/#use-x-forwarded-host

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_json_api',
    'social_django',
    'core.apps.CoreConfig',
    'access.apps.AccessConfig',
    'itam.apps.ItamConfig',
    'settings.apps.SettingsConfig',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'config_management.apps.ConfigManagementConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.get_request.RequestMiddleware',
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

LOGIN_REDIRECT_URL = "home"
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

SITE_TITLE = "Site Title"


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
            'rest_framework_json_api.filters.QueryParameterValidationFilter',
            'rest_framework_json_api.filters.OrderingFilter',
            'rest_framework_json_api.django_filters.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',
        ),
        'SEARCH_PARAM': 'filter[search]',
        # 'TEST_REQUEST_RENDERER_CLASSES': (
        #     'rest_framework_json_api.renderers.JSONRenderer',
        # ),
        # 'TEST_REQUEST_DEFAULT_FORMAT': 'vnd.api+json'
        'TEST_REQUEST_DEFAULT_FORMAT': 'json',
        'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    }

    SPECTACULAR_SETTINGS = {
        'TITLE': 'ITSM API',
        'DESCRIPTION': """This UI is intended to serve as the API documentation.

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
        'VERSION': '1.0.0',
        'SERVE_INCLUDE_SCHEMA': False,

        'SWAGGER_UI_DIST': 'SIDECAR',
        'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
        'REDOC_DIST': 'SIDECAR',
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

    # Apps Under Development
    INSTALLED_APPS += [
        'information.apps.InformationConfig',
        'project_management.apps.ProjectManagementConfig',
    ]


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
