from centurion_feature_flag.urls.routers import DefaultRouter

from devops.viewsets import (
    feature_flag,
    git_group,
    git_repository,
)



app_name = "devops"

router = DefaultRouter(trailing_slash=False)

router.register(
    prefix = 'feature_flag', viewset = feature_flag.ViewSet,
    basename = '_api_featureflag'
)
router.register(
    prefix = r'git_repository(?:/(?P<git_provider>gitlab|github))?',
    viewset = git_repository.ViewSet,
    feature_flag = '2025-00001', basename = '_api_v2_git_repository'
)
router.register(
    prefix = 'git_group', viewset = git_group.ViewSet,
    feature_flag = '2025-00001', basename = '_api_gitgroup'
)

urlpatterns = router.urls
