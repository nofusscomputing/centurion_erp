from rest_framework.routers import DefaultRouter


app_name = "hr"

from human_resources.viewsets import index as HumanResourcesHome

router = DefaultRouter(trailing_slash=False)

router.register('', HumanResourcesHome.Index, basename='_api_v2_access_home')

urlpatterns = router.urls
