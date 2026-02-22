from django.apps import apps

from centurion_feature_flag.urls.routers import DefaultRouter

from core.viewsets import (
    audit_history,
    ticket,
    ticket_comment,
    ticket_comment_depreciated,
    ticket_dependency,
    ticket_linked_item,
    ticket_model_link,
    related_ticket,

)


ticket_type_names = ''
ticket_comment_names = ''

for model in apps.get_models():


    if issubclass(model, ticket.TicketBase):

        ticket_type_names += model._meta.model_name + '|'


    if issubclass(model, ticket_comment.TicketCommentBase):

        ticket_comment_names += model._meta.model_name + '|'


ticket_comment_names = str(ticket_comment_names)[:-1]
ticket_type_names = str(ticket_type_names)[:-1]


# app_name = "core"


router: DefaultRouter = DefaultRouter(trailing_slash=False)



router.register(
    '/history', audit_history.NoDocsViewSet,
    basename = '_api_centurionaudit'
)



router.register(
    prefix=f'/ticket', viewset = ticket.NoDocsViewSet,
    feature_flag = '2025-00006', basename = '_api_ticketbase'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/comment', viewset = ticket_comment.NoDocsViewSet,
    feature_flag = '2025-00006', basename = '_api_ticket_comment_base'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/comment/(?P<parent_id>[0-9]+)/threads',
    viewset = ticket_comment.ViewSet,
    feature_flag = '2025-00006', basename = '_api_ticket_comment_base_thread'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/comments', viewset = ticket_comment_depreciated.ViewSet,
    basename = '_api_v2_ticket_comment'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/comments/(?P<parent_id>[0-9]+)/threads',
    viewset = ticket_comment_depreciated.ViewSet,
    basename = '_api_v2_ticket_comment_threads'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/linked_item', viewset = ticket_linked_item.ViewSet,
    basename = '_api_v2_ticket_linked_item'
)
router.register(
    prefix=f'/ticket/(?P<model_name>[{ticket_type_names}]+)/(?P<model_id>[0-9]+)/models', viewset = ticket_model_link.ViewSet,
    feature_flag = '2025-00006', basename = '_api_modelticket'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/related_ticket', viewset = related_ticket.ViewSet,
    basename = '_api_v2_ticket_related'
)
router.register(
    prefix=f'/ticket/(?P<ticket_id>[0-9]+)/(?P<model_name>[{ticket_comment_names}]+)',
    viewset = ticket_comment.ViewSet,
    feature_flag = '2025-00006', basename = '_api_ticket_comment_base_sub'
)
router.register(
    prefix=f'/ticket/(?P<ticket_id>[0-9]+)/(?P<model_name>[{ticket_comment_names} \
        ]+)/(?P<parent_id>[0-9]+)/threads',
    viewset = ticket_comment.ViewSet,
    feature_flag = '2025-00006', basename = '_api_ticket_comment_base_sub_thread'
)
router.register(
    prefix = '/ticket/(?P<ticket_id>[0-9]+)/ticket_dependency', viewset = ticket_dependency.ViewSet,
    basename = '_api_ticketdependency'
)
router.register(
    prefix = '/(?P<item_class>[a-z_]+)/(?P<item_id>[0-9]+)/item_ticket',
    viewset = ticket_linked_item.ViewSet,
    basename = '_api_v2_item_tickets'
)


urlpatterns = router.urls
