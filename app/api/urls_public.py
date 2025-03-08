from django.urls import include, path

from rest_framework.routers import DefaultRouter


from api.viewsets import (
    public
)


app_name = "public"

router = DefaultRouter(trailing_slash=False)

router.register('', public.Index, basename='_public_api_v2')

urlpatterns = router.urls
