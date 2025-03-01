from rest_framework.routers import DefaultRouter

from devops.viewsets import (
    feature_flag,
)



app_name = "devops"

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls
