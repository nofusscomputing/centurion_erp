from rest_framework.routers import DefaultRouter

from devops.viewsets import (
    feature_flag,
)



app_name = "devops"

router = DefaultRouter(trailing_slash=False)

router.register('feature_flag', feature_flag.ViewSet, basename='_api_v2_feature_flag')

urlpatterns = router.urls
