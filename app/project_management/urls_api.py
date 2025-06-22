from centurion_feature_flag.urls.routers import DefaultRouter

from project_management.viewsets import (
    index as project_management,
    project,
    project_milestone,
    project_task,
)



# app_name = "project_management"


router: DefaultRouter = DefaultRouter(trailing_slash=False)


router.register(
    prefix = '', viewset = project_management.Index,
    basename = '_api_v2_project_management_home'
)
router.register(
    prefix = 'project', viewset = project.ViewSet,
    basename = '_api_project'
)
router.register(
    prefix = 'project/(?P<project_id>[0-9]+)/milestone',
    viewset = project_milestone.ViewSet,
    basename = '_api_projectmilestone'
)
router.register(
    prefix = 'project/(?P<project_id>[0-9]+)/project_task',
    viewset = project_task.ViewSet,
    basename = '_api_v2_ticket_project_task'
)


urlpatterns = router.urls
