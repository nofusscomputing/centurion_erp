from centurion_feature_flag.urls.routers import DefaultRouter


app_name = "hr"

from human_resources.viewsets import index as HumanResourcesHome

router = DefaultRouter(trailing_slash=False)

router.register('', HumanResourcesHome.Index, basename='_api_human_resources_home')

urlpatterns = router.urls
