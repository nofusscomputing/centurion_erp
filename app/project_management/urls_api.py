from django.apps import apps

from centurion_feature_flag.urls.routers import DefaultRouter

from core.viewsets import (
    ticket
)

from project_management.viewsets import (
    index as project_management,
    project,
    project_milestone,
    project_task,
)


# app_name = "project_management"



router: DefaultRouter = DefaultRouter(trailing_slash=False)


ticket_type_names = ''

for model in apps.get_models():

    if issubclass(model, ticket.TicketBase):

        if(
            (not router._feature_flagging['2025-00009'] and 'change' in model._meta.model_name)
            or (not router._feature_flagging['2025-00010'] and 'incident' in model._meta.model_name)
            or (not router._feature_flagging['2025-00011'] and 'problem' in model._meta.model_name)
            or (not router._feature_flagging['2026-00012'] and 'request' in model._meta.model_name)
        ):
            continue


        ticket_type_names += model._meta.model_name + '|'


ticket_type_names = str(ticket_type_names)[:-1]


router.register(
    prefix = '', viewset = project_management.Index,
    basename = '_api_v2_project_management_home'
)
router.register(
    prefix = '/project', viewset = project.ViewSet,
    basename = '_api_project'
)
router.register(
    prefix = '/project/(?P<project_id>[0-9]+)/milestone',
    viewset = project_milestone.ViewSet,
    basename = '_api_projectmilestone'
)
router.register(
    prefix = '/project/(?P<project_id>[0-9]+)/project_task',
    viewset = project_task.ViewSet,
    basename = '_api_v2_ticket_project_task'
)

router.register(
    prefix = f'/project/(?P<project_id>[0-9]+)/ticket/(?P<model_name>[{ticket_type_names}]+)',
    viewset = ticket.ViewSet,
    basename = '_api_project_ticket_sub'
)


urlpatterns = router.urls
