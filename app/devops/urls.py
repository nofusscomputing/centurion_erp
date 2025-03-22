from centurion_feature_flag.urls.routers import DefaultRouter

from devops.viewsets import (
    feature_flag,
    feature_flag_notes,
    git_group,
    git_group_notes,
    git_repository,
    github_repository_notes,
    gitlab_repository_notes
)



app_name = "devops"

router = DefaultRouter(trailing_slash=False)

router.register('feature_flag', feature_flag.ViewSet, basename='_api_v2_feature_flag')
router.register('feature_flag/(?P<model_id>[0-9]+)/notes', feature_flag_notes.ViewSet, basename='_api_v2_feature_flag_note')

router.register(r'git_repository(?:/(?P<git_provider>gitlab|github))?', git_repository.ViewSet, feature_flag = '2025-00001', basename='_api_v2_git_repository')

router.register('git_group', git_group.ViewSet, feature_flag = '2025-00001', basename='_api_v2_git_group')
router.register('git_group/notes', git_group_notes.ViewSet, feature_flag = '2025-00001', basename='_api_v2_git_group_notes')

router.register('git_repository/github/notes', github_repository_notes.ViewSet, feature_flag = '2025-00001', basename='_api_v2_github_repository_notes')
router.register('git_repository/gitlab/notes', gitlab_repository_notes.ViewSet, feature_flag = '2025-00001', basename='_api_v2_gitlab_repository_notes')

urlpatterns = router.urls
