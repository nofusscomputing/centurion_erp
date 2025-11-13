from django.apps import apps
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from centurion_feature_flag.urls.routers import DefaultRouter

from api.viewsets import (
    index as v2
)

from centurion.viewsets.base import (
    index as base_index_v2,
    content_type as content_type_v2,
    group,
    permission,
    user
)

from core.viewsets import (
    ticket,
    audit_history,
    centurion_model_notes,
    ticket_model_link,
)

app_name = "API"


history_type_names = ''
history_app_labels = ''
notes_type_names = ''
notes_app_labels = ''
ticket_model_links_app_labels = ''
ticket_model_links_type_names = ''
ticket_app_names = ''
ticket_type_names = ''

for model in apps.get_models():

    if getattr(model, '_audit_enabled', False):

        history_type_names += model._meta.model_name + '|'

        if model._meta.app_label not in history_app_labels:

            history_app_labels += model._meta.app_label + '|'


    if getattr(model, '_notes_enabled', False):

        notes_type_names += model._meta.model_name + '|'

        if model._meta.app_label not in notes_app_labels:

            notes_app_labels += model._meta.app_label + '|'

    if getattr(model, '_ticket_linkable', False):

        ticket_model_links_type_names += model._meta.model_name + '|'

        if model._meta.app_label not in ticket_model_links_app_labels:

            ticket_model_links_app_labels += model._meta.app_label + '|'

    if issubclass(model, ticket.TicketBase):
        ticket_app_names += model._meta.app_label + '|'
        ticket_type_names += model._meta.sub_model_type + '|'


history_app_labels = str(history_app_labels)[:-1]
history_type_names = str(history_type_names)[:-1]

notes_app_labels = str(notes_app_labels)[:-1]
notes_type_names = str(notes_type_names)[:-1]

ticket_model_links_app_labels = str(ticket_model_links_app_labels)[:-1]
ticket_model_links_type_names = str(ticket_model_links_type_names)[:-1]

ticket_app_names = str(ticket_app_names)[:-1]
ticket_type_names = str(ticket_type_names)[:-1]

router = DefaultRouter(trailing_slash=False)

if not router._feature_flagging['2025-00006']:
    ticket_type_names = str( ticket_type_names ).replace('request', '').replace('||', '')


if not router._feature_flagging['2025-00009']:
    ticket_type_names = str( ticket_type_names ).replace('change', '').replace('||', '')



router.register('', v2.Index, basename='_api_v2_home')


router.register('/base', base_index_v2.Index, basename='_api_v2_base_home')
router.register('/base/content_type', content_type_v2.ViewSet, basename='_api_v2_content_type')
router.register('/base/group', group.ViewSet, basename='_api_group')
router.register('/base/permission', permission.ViewSet, basename='_api_permission')
router.register('/base/user', user.ViewSet, basename='_api_user')



router.register(
    prefix = f'/(?P<app_label>[{history_app_labels}]+)/(?P<model_name>[{history_type_names} \
        ]+)/(?P<model_id>[0-9]+)/history',
    viewset = audit_history.ViewSet,
    basename = '_api_centurionaudit_sub'
)

router.register(
    prefix = f'/(?P<app_label>[{notes_app_labels}]+)/(?P<model_name>[{notes_type_names} \
        ]+)/(?P<model_id>[0-9]+)/notes',
    viewset = centurion_model_notes.ViewSet,
    basename = '_api_centurionmodelnote_sub'
)

router.register(
    prefix = f'/(?P<app_label>[{ticket_model_links_app_labels} \
        ]+)/(?P<model_name>[{ticket_model_links_type_names}]+)/(?P<model_id>[0-9]+)/tickets',
    viewset = ticket_model_link.ViewSet,
    feature_flag = '2025-00006', basename = '_api_modelticket_sub'
)

router.register(
    prefix = f'/(?P<app_label>[{ticket_app_names} \
        ]+)/ticket/(?P<ticket_type>[{ticket_type_names}]+)',
    viewset = ticket.ViewSet,
    feature_flag = '2025-00006', basename = '_api_ticketbase_sub'
)


urlpatterns = [

    path('/schema', SpectacularAPIView.as_view(api_version='v2'), name='schema-v2',),
    path('/docs', SpectacularSwaggerView.as_view(url_name='schema-v2'), name='_api_v2_docs'),

]

urlpatterns += router.urls

urlpatterns += [
    path(route = "/access", view = include("access.urls_api")),
    path(route = "/accounting", view = include("accounting.urls")),
    path(route = "/assistance", view = include("assistance.urls_api")),
    path(route = "/config_management", view = include("config_management.urls_api")),
    path(route = "/core", view = include("core.urls_api")),
    path(route = "/devops", view = include("devops.urls")),
    path(route = "/hr", view = include('human_resources.urls')),
    path(route = "/itam", view = include("itam.urls_api")),
    path(route = "/itim", view = include("itim.urls_api")),
    path(route = "/project_management", view = include("project_management.urls_api")),
    path(route = "/settings", view = include("settings.urls_api")),
    path(route = '/public', view = include('api.urls_public')),
]
