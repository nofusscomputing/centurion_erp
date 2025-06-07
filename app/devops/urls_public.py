from rest_framework.routers import SimpleRouter

from devops.viewsets import (
    feature_flag_endpoints,
    public_feature_flag,
)



app_name = "devops"

router = SimpleRouter(trailing_slash=False)

router.register('flags', feature_flag_endpoints.Index, basename='_api_v2_flags')

router.register('(?P<organization_id>[0-9]+)/flags/(?P<software_id>[0-9]+)', public_feature_flag.ViewSet, basename='_public_api_v2_feature_flag')

urlpatterns = router.urls
