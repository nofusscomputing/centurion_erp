from app import settings
from centurion_feature_flag.lib.feature_flag import CenturionFeatureFlagging



class FeatureFlagMiddleware:

    _feature_flagging: CenturionFeatureFlagging = None


    def __init__(self, get_response):

        self.get_response = get_response

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


    def __call__(self, request):

        if(
            '/flags/' not in request.path
            and self._feature_flagging is not None
        ):

            self._feature_flagging.get()

            setattr(request, 'feature_flag', self._feature_flagging)

        return self.get_response(request)

    