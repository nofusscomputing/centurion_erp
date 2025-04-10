from centurion_feature_flag.urls.routers import DefaultRouter


app_name = "accounting"

router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls
