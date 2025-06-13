import re

from centurion.urls import urlpatterns

from django.conf import settings
from django.urls import URLPattern, URLResolver

from access.models.tenant import Tenant as Organization

from settings.models.user_settings import UserSettings


def build_details(context) -> dict:

    return {
        'project_url': settings.BUILD_REPO,
        'sha': settings.BUILD_SHA,
        'version': settings.BUILD_VERSION,
    }


def request(request):
    return request.get_full_path()


def social_backends(request):
    """ Fetch Backend Names

    Required for use on the login page to dynamically build the social auth URLS

    Returns:
        list(str): backend name
    """
    from importlib import import_module

    social_backends = []

    if hasattr(settings, 'SSO_BACKENDS'):

        for backend in settings.SSO_BACKENDS:

            paths = str(backend).split('.')

            module = import_module(paths[0] + '.' + paths[1] + '.' + paths[2])

            backend_class = getattr(module, paths[3])
            backend = backend_class.name

            social_backends += [ str(backend) ]

    return social_backends


def user_settings(context) -> int:
    """ Provides the settings ID for the current user.

    If user settings object doesn't exist, it's probably a new user. So create their settings row.

    Returns:
        int: model usersettings Primary Key
    """
    if context.user.is_authenticated:

        settings = UserSettings.objects.filter(user=context.user)

        if not settings.exists():

            UserSettings.objects.create(user=context.user)

            settings = UserSettings.objects.filter(user=context.user)

        return settings[0].pk

    return None


def common(context):

    return {
        'build_details': build_details(context),
        'social_backends': social_backends(context),
        'user_settings': user_settings(context),
    }
