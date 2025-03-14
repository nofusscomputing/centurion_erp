from django.urls.conf import (
    _path as _django_path,
    include,    # pylint: disable=W0611:unused-import
    partial,
    RegexPattern as DjangoRegexPattern,
    RoutePattern as DjangoRoutePattern,
)

from app import settings

from centurion_feature_flag.lib.feature_flag import CenturionFeatureFlagging
from centurion_feature_flag.views.disabled import FeatureFlagView



_feature_flagging: CenturionFeatureFlagging = None

if getattr(settings,'feature_flag', None):

    _feature_flagging = CenturionFeatureFlagging(
            url = settings.feature_flag['url'],
            user_agent = settings.feature_flag['user_agent'],
            cache_dir =settings.feature_flag['cache_dir'],
            unique_id = settings.feature_flag.get('unique_id', None),
            version = settings.feature_flag.get('version', None),
        )

    _feature_flagging.get()



def _path(route, view, kwargs=None, name=None, Pattern=None, feature_flag: str =None):


    if feature_flag is not None:

        if not _feature_flagging[feature_flag]:

            view = FeatureFlagView.as_view()

    return _django_path(route, view, kwargs=kwargs, name=name, Pattern=Pattern)



path = partial(_path, Pattern=DjangoRoutePattern)
re_path = partial(_path, Pattern=DjangoRegexPattern)
