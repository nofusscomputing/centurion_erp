from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from .views import index



app_name = "API"


router = DefaultRouter(trailing_slash=False)

router.register('', index.Index, basename='_api_home')


urlpatterns = [

]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls
