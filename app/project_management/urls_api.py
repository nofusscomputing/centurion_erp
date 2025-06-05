from centurion_feature_flag.urls.routers import DefaultRouter

from project_management.viewsets import (
    index as project_management_v2,
    project as project_v2,
    project_milestone as project_milestone_v2,
    project_task,
)



# app_name = "project_management"


router: DefaultRouter = DefaultRouter(trailing_slash=False)


router.register(
    prefix = '', viewset = project_management_v2.Index,
    basename = '_api_v2_project_management_home'
)
router.register(
    prefix = 'project', viewset = project_v2.ViewSet,
    basename = '_api_v2_project'
)
router.register(
    prefix = 'project/(?P<project_id>[0-9]+)/milestone',
    viewset = project_milestone_v2.ViewSet,
    basename = '_api_v2_project_milestone'
)
router.register(
    prefix = 'project/(?P<project_id>[0-9]+)/project_task',
    viewset = project_task.ViewSet,
    basename = '_api_v2_ticket_project_task'
)


urlpatterns = router.urls
