import re

from app.urls import urlpatterns

from django.conf import settings
from django.urls import URLPattern, URLResolver

from settings.models.user_settings import UserSettings


def build_details(context) -> dict:

    return {
        'project_url': settings.BUILD_REPO,
        'sha': settings.BUILD_SHA,
        'version': settings.BUILD_VERSION,
    }


def request(request):
    return request.get_full_path()


def user_settings(context) -> int:
    """ Provides the settings ID for the current user

    Returns:
        int: model usersettings Primary Key
    """
    if context.user.is_authenticated:

        settings = UserSettings.objects.filter(user=context.user)

        return settings[0].pk

    return None


def nav_items(context) -> list(dict()):
    """ Fetch All Project URLs

    Collect the project URLs for use in creating the site navigation.

    The returned list contains a dictionary with the following items:
        name: {str} Group Name
        urls: {list} List of URLs for the group
        is_active: {bool} if any of the links in this group are active

    Each group url list item contains a dicionary with the following items:
        name: {str} The display name for the link
        url: {str} link URL
        is_active: {bool} if this link is the active URL

    Returns:
        _type_: _description_
    """

    dnav = []
    re_pattern = re.compile('[a-z/0-9]+')
    
    for nav_group in urlpatterns:

        group_active = False

        ignored_apps = [
            'admin',
            'djdt',     # Debug application
        ] 

        nav_items = []

        if (
            isinstance(nav_group, URLPattern)
        ):

            group_name = str(nav_group.name)

        elif (
            isinstance(nav_group, URLResolver)
        ):

            if nav_group.app_name is not None and nav_group.app_name not in ignored_apps:

                group_name = str(nav_group.app_name)

                for pattern in nav_group.url_patterns:

                    is_active = False

                    url = '/' + str(nav_group.pattern) + str(pattern.pattern)

                    if str(context.path).startswith(url):

                        is_active = True
                    
                    if str(context.path).startswith('/' + str(nav_group.pattern)):
                        group_active = True

                    if (
                        pattern.pattern.name is not None
                          and
                        not str(pattern.pattern.name).startswith('_')
                    ):

                        name = str(pattern.name)

                        nav_items = nav_items + [ {
                            'name': name,
                            'url': url,
                            'is_active': is_active
                            } ]

        if len(nav_items) > 0:

            dnav = dnav + [{
                'name': group_name,
                'urls': nav_items,
                'is_active': group_active
                }]


    return dnav


def common(context):

    return {
        'build_details': build_details(context),
        'nav_items': nav_items(context),
        'user_settings': user_settings(context),
    }
