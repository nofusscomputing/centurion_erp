from rest_framework.routers import DefaultRouter


app_name = "hr"

router = DefaultRouter(trailing_slash=False)


urlpatterns = router.urls
