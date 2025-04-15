from centurion_feature_flag.urls.routers import DefaultRouter


app_name = "hr"

from human_resources.viewsets import index as HumanResourcesHome

router = DefaultRouter(trailing_slash=False)

router.register('', HumanResourcesHome.Index, feature_flag = '2025-00005', basename='_api_v2_access_home')

urlpatterns = router.urls
