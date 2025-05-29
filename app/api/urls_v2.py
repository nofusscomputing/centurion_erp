from django.apps import apps
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from centurion_feature_flag.urls.routers import DefaultRouter

from api.viewsets import (
    auth_token,
    index as v2
)

from centurion.viewsets.base import (
    index as base_index_v2,
    content_type as content_type_v2,
    permisson as permission_v2,
    user as user_v2
)

from assistance.viewsets import (
    knowledge_base_category as knowledge_base_category_v2,
    knowledge_base_category_notes,
)

from core.viewsets import (
    audit_history,
    celery_log as celery_log_v2,
    history as history_v2,
    manufacturer as manufacturer_v2,
    manufacturer_notes,
    ticket,
    ticket_category,
    ticket_category_notes,
    ticket_comment,
    ticket_comment_category,
    ticket_comment_category_notes,

)

from itam.viewsets import (
    device_model as device_model_v2,
    device_model_notes,
    device_type as device_type_v2,
    device_type_notes,
    software_category as software_category_v2,
    software_category_notes,
)

from itim.viewsets import (
    cluster_type as cluster_type_v2,
    cluster_type_notes,
    port as port_v2,
    port_notes,
)

from project_management.viewsets import (
    index as project_management_v2,
    project as project_v2,
    project_milestone as project_milestone_v2,
    project_milestone_notes,
    project_notes,
    project_state as project_state_v2,
    project_state_notes,
    project_task,
    project_type as project_type_v2,
    project_type_notes,
)

from settings.viewsets import (
    app_settings as app_settings_v2,
    external_link as external_link_v2,
    external_link_notes,
    index as settings_index_v2,
    user_settings as user_settings_v2
)

app_name = "API"


router = DefaultRouter(trailing_slash=False)


router.register('', v2.Index, basename='_api_v2_home')

history_type_names = ''
history_app_labels = ''
ticket_type_names = ''
ticket_comment_names = ''

for model in apps.get_models():

    if getattr(model, '_audit_enabled', False):

        history_type_names += model._meta.model_name + '|'

        if model._meta.app_label not in history_app_labels:

            history_app_labels += model._meta.app_label + '|'


    if issubclass(model, ticket.TicketBase):

        ticket_type_names += model._meta.sub_model_type + '|'


    if issubclass(model, ticket_comment.TicketCommentBase):

        ticket_comment_names += model._meta.sub_model_type + '|'

# pylint: disable=C0301:line-too-long


router.register('base', base_index_v2.Index, basename='_api_v2_base_home')
router.register('base/content_type', content_type_v2.ViewSet, basename='_api_v2_content_type')
router.register('base/permission', permission_v2.ViewSet, basename='_api_v2_permission')
router.register('base/user', user_v2.ViewSet, basename='_api_v2_user')



router.register(
    prefix = f'(?P<app_label>[{history_app_labels}]+)/(?P<model_name>[{history_type_names}]+)/(?P<model_id>[0-9]+)/history',
    viewset = audit_history.ViewSet,
    basename = '_api_centurionaudit_sub'
)
router.register(
    prefix = '(?P<app_label>[a-z_]+)/(?P<model_name>.+)/(?P<model_id>[0-9]+)/history',
    viewset = history_v2.ViewSet,
    basename = '_api_v2_model_history'
)


router.register('project_management', project_management_v2.Index, basename='_api_v2_project_management_home')
router.register('project_management/project', project_v2.ViewSet, basename='_api_v2_project')
router.register('project_management/project/(?P<project_id>[0-9]+)/milestone', project_milestone_v2.ViewSet, basename='_api_v2_project_milestone')
router.register('project_management/project/(?P<project_id>[0-9]+)/milestone/(?P<model_id>[0-9]+)/notes', project_milestone_notes.ViewSet, basename='_api_v2_project_milestone_note')
router.register('project_management/project/(?P<model_id>[0-9]+)/notes', project_notes.ViewSet, basename='_api_v2_project_note')
router.register('project_management/project/(?P<project_id>[0-9]+)/project_task', project_task.ViewSet, basename='_api_v2_ticket_project_task')


router.register('settings', settings_index_v2.Index, basename='_api_v2_settings_home')
router.register('settings/app_settings', app_settings_v2.ViewSet, basename='_api_v2_app_settings')
router.register('settings/celery_log', celery_log_v2.ViewSet, basename='_api_v2_celery_log')
router.register('settings/cluster_type', cluster_type_v2.ViewSet, basename='_api_v2_cluster_type')
router.register('settings/cluster_type/(?P<model_id>[0-9]+)/notes', cluster_type_notes.ViewSet, basename='_api_v2_cluster_type_note')
router.register('settings/device_model', device_model_v2.ViewSet, basename='_api_v2_device_model')
router.register('settings/device_model/(?P<model_id>[0-9]+)/notes', device_model_notes.ViewSet, basename='_api_v2_device_model_note')
router.register('settings/device_type', device_type_v2.ViewSet, basename='_api_v2_device_type')
router.register('settings/device_type/(?P<model_id>[0-9]+)/notes', device_type_notes.ViewSet, basename='_api_v2_device_type_note')
router.register('settings/external_link', external_link_v2.ViewSet, basename='_api_v2_external_link')
router.register('settings/external_link/(?P<model_id>[0-9]+)/notes', external_link_notes.ViewSet, basename='_api_v2_external_link_note')
router.register('settings/knowledge_base_category', knowledge_base_category_v2.ViewSet, basename='_api_v2_knowledge_base_category')
router.register('settings/knowledge_base_category/(?P<model_id>[0-9]+)/notes', knowledge_base_category_notes.ViewSet, basename='_api_v2_knowledge_base_category_note')
router.register('settings/manufacturer', manufacturer_v2.ViewSet, basename='_api_v2_manufacturer')
router.register('settings/manufacturer/(?P<model_id>[0-9]+)/notes', manufacturer_notes.ViewSet, basename='_api_v2_manufacturer_note')
router.register('settings/port', port_v2.ViewSet, basename='_api_v2_port')
router.register('settings/port/(?P<model_id>[0-9]+)/notes', port_notes.ViewSet, basename='_api_v2_port_note')
router.register('settings/project_state', project_state_v2.ViewSet, basename='_api_v2_project_state')
router.register('settings/project_state/(?P<model_id>[0-9]+)/notes', project_state_notes.ViewSet, basename='_api_v2_project_state_note')
router.register('settings/project_type', project_type_v2.ViewSet, basename='_api_v2_project_type')
router.register('settings/project_type/(?P<model_id>[0-9]+)/notes', project_type_notes.ViewSet, basename='_api_v2_project_type_note')
router.register('settings/software_category', software_category_v2.ViewSet, basename='_api_v2_software_category')
router.register('settings/software_category/(?P<model_id>[0-9]+)/notes', software_category_notes.ViewSet, basename='_api_v2_software_category_note')
router.register('settings/ticket_category', ticket_category.ViewSet, basename='_api_v2_ticket_category')
router.register('settings/ticket_category/(?P<model_id>[0-9]+)/notes', ticket_category_notes.ViewSet, basename='_api_v2_ticket_category_note')
router.register('settings/ticket_comment_category', ticket_comment_category.ViewSet, basename='_api_v2_ticket_comment_category')
router.register('settings/ticket_comment_category/(?P<model_id>[0-9]+)/notes', ticket_comment_category_notes.ViewSet, basename='_api_v2_ticket_comment_category_note')
router.register('settings/user_settings', user_settings_v2.ViewSet, basename='_api_v2_user_settings')
router.register('settings/user_settings/(?P<model_id>[0-9]+)/token', auth_token.ViewSet, basename='_api_v2_user_settings_token')


urlpatterns = [

    path('schema', SpectacularAPIView.as_view(api_version='v2'), name='schema-v2',),
    path('docs', SpectacularSwaggerView.as_view(url_name='schema-v2'), name='_api_v2_docs'),

]

urlpatterns += router.urls

urlpatterns += [
    path(route = "access/", view = include("access.urls_api")),
    path(route = "accounting/", view = include("accounting.urls")),
    path(route = "assistance/", view = include("assistance.urls_api")),
    path(route = "config_management/", view = include("config_management.urls_api")),
    path(route = "core/", view = include("core.urls_api")),
    path(route = "devops/", view = include("devops.urls")),
    path(route = "itam/", view = include("itam.urls_api")),
    path(route = "itim/", view = include("itim.urls_api")),
    path(route = "hr/", view = include('human_resources.urls')),
    path(route = 'public/', view = include('api.urls_public')),
]
