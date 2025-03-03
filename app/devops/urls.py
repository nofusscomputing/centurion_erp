from rest_framework.routers import DefaultRouter

from devops.viewsets import (
    feature_flag,
    feature_flag_notes,
)



app_name = "devops"

router = DefaultRouter(trailing_slash=False)

router.register('feature_flag', feature_flag.ViewSet, basename='_api_v2_feature_flag')
router.register('feature_flag/(?P<model_id>[0-9]+)/notes', feature_flag_notes.ViewSet, basename='_api_v2_feature_flag_note')

urlpatterns = router.urls
