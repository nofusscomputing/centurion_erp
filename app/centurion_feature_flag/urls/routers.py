from rest_framework.routers import (
    APIRootView as DRFAPIRootView,
    BaseRouter as DRFBaseRouter,
    DefaultRouter as DRFDefaultRouter,
    SimpleRouter as DRFSimpleRouter,
)

from centurion import settings

from centurion_feature_flag.lib.feature_flag import CenturionFeatureFlagging



class BaseRouter(
    DRFBaseRouter,
):


    _feature_flagging: CenturionFeatureFlagging = None


    def register(self, prefix, viewset, feature_flag=None, basename=None):

        enabled = True

        if feature_flag is not None:

            if not self._feature_flagging.get('feature_flag', None):

                enabled = False

        if(
            enabled
            or feature_flag is None
        ):

            super().register(prefix, viewset, basename=basename)



class APIRootView(
    DRFAPIRootView,
):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        if getattr(settings,'feature_flag', None):

            self._feature_flagging = CenturionFeatureFlagging(
                url = settings.feature_flag['url'],
                user_agent = settings.feature_flag['user_agent'],
                cache_dir =settings.feature_flag['cache_dir'],
                disable_downloading = settings.feature_flag.get('disable_downloading', False),
                unique_id = settings.feature_flag.get('unique_id', None),
                version = settings.feature_flag.get('version', None),
                over_rides = settings.feature_flag.get('over_rides', None),
            )



class SimpleRouter(
    BaseRouter,
    DRFSimpleRouter,
):

    def __init__(self, trailing_slash=True, use_regex_path=True):

        super().__init__(trailing_slash=trailing_slash, use_regex_path=use_regex_path)

        if getattr(settings,'feature_flag', None):

            self._feature_flagging = CenturionFeatureFlagging(
                url = settings.feature_flag['url'],
                user_agent = settings.feature_flag['user_agent'],
                cache_dir =settings.feature_flag['cache_dir'],
                disable_downloading = settings.feature_flag.get('disable_downloading', False),
                unique_id = settings.feature_flag.get('unique_id', None),
                version = settings.feature_flag.get('version', None),
                over_rides = settings.feature_flag.get('over_rides', None),
            )

            self._feature_flagging.get()



class DefaultRouter(
    BaseRouter,
    DRFDefaultRouter,
):



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if getattr(settings,'feature_flag', None):

            self._feature_flagging = CenturionFeatureFlagging(
                url = settings.feature_flag['url'],
                user_agent = settings.feature_flag['user_agent'],
                cache_dir =settings.feature_flag['cache_dir'],
                disable_downloading = settings.feature_flag.get('disable_downloading', False),
                unique_id = settings.feature_flag.get('unique_id', None),
                version = settings.feature_flag.get('version', None),
                over_rides = settings.feature_flag.get('over_rides', None),
            )

            self._feature_flagging.get()
