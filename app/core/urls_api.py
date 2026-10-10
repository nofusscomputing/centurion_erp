from django.apps import apps

from centurion_feature_flag.urls.routers import DefaultRouter

from core.viewsets import (
    audit_history,
    ticket,
    ticket_comment,
    ticket_dependency,
    ticket_model_link,

)


# app_name = "core"


router: DefaultRouter = DefaultRouter(trailing_slash=False)


ticket_type_names = ''
ticket_comment_names = ''

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


    if issubclass(model, ticket_comment.TicketCommentBase):

        ticket_comment_names += model._meta.model_name + '|'


ticket_comment_names = str(ticket_comment_names)[:-1]
ticket_type_names = str(ticket_type_names)[:-1]



router.register(
    '/history', audit_history.NoDocsViewSet,
    basename = '_api_centurionaudit'
)



router.register(
    prefix=f'/ticket', viewset = ticket.NoDocsViewSet,
    basename = '_api_ticketbase'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/comment', viewset = ticket_comment.NoDocsViewSet,
    basename = '_api_ticket_comment_base'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/comment/(?P<parent_id>[0-9]+)/threads',
    viewset = ticket_comment.ViewSet,
    basename = '_api_ticket_comment_base_thread'
)
router.register(
    prefix=(f'/ticket/(?P<ticket_id>[0-9]+)/(?P<model_name>({ticket_comment_names}'
        ')+)/(?P<parent_id>[0-9]+)/threads'),
    viewset = ticket_comment.ViewSet,
    basename = '_api_ticket_comment_base_thread_sub'
)
router.register(
    prefix=f'/ticket/(?P<model_name>({ticket_type_names})+)/(?P<model_id>[0-9]+)/models', viewset = ticket_model_link.ViewSet,
    basename = '_api_modelticket'
)
router.register(
    prefix=f'/ticket/(?P<ticket_id>[0-9]+)/(?P<model_name>({ticket_comment_names})+)',
    viewset = ticket_comment.ViewSet,
    basename = '_api_ticket_comment_base_sub'
)
router.register(
    prefix=(f'/ticket/(?P<ticket_id>[0-9]+)/(?P<model_name>({ticket_comment_names}'
        ')+)/(?P<parent_id>[0-9]+)/threads'),
    viewset = ticket_comment.ViewSet,
    basename = '_api_ticket_comment_base_sub_thread'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/ticket_dependency', viewset = ticket_dependency.ViewSet,
    basename = '_api_ticketdependency'
)


urlpatterns = router.urls
