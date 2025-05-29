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

from config_management.viewsets import (
    index as config_management_v2,
    config_group as config_group_v2,
    config_group_notes,
    config_group_software as config_group_software_v2
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
    ticket_comment_depreciated,
    ticket_comment_category,
    ticket_comment_category_notes,
    ticket_linked_item,
    related_ticket,

)

from devops.viewsets import (
    software_enable_feature_flag,
)

from itam.viewsets import (
    index as itam_index_v2,
    device as device_v2,
    device_model as device_model_v2,
    device_model_notes,
    device_notes,
    device_type as device_type_v2,
    device_type_notes,
    device_software as device_software_v2,
    device_operating_system,
    inventory,
    operating_system as operating_system_v2,
    operating_system_notes,
    operating_system_version as operating_system_version_v2,
    operating_system_version_notes,
    software as software_v2,
    software_category as software_category_v2,
    software_category_notes,
    software_notes,
    software_version as software_version_v2,
    software_version_notes,
)

from itim.viewsets import (
    index as itim_v2,
    change,
    cluster as cluster_v2,
    cluster_notes,
    cluster_type as cluster_type_v2,
    cluster_type_notes,
    incident,
    port as port_v2,
    port_notes,
    problem,
    service as service_v2,
    service_cluster,
    service_device as service_device_v2,
    service_notes,
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


router.register('config_management', config_management_v2.Index, basename='_api_v2_config_management_home')
router.register('config_management/group', config_group_v2.ViewSet, basename='_api_v2_config_group')
router.register('config_management/group/(?P<parent_group>[0-9]+)/child_group', config_group_v2.ViewSet, basename='_api_v2_config_group_child')
router.register('config_management/group/(?P<model_id>[0-9]+)/notes', config_group_notes.ViewSet, basename='_api_v2_config_group_note')
router.register('config_management/group/(?P<config_group_id>[0-9]+)/software', config_group_software_v2.ViewSet, basename='_api_v2_config_group_software')


history_type_names = str(history_type_names)[:-1]
router.register(f'(?P<app_label>[{history_app_labels}]+)/(?P<model_name>[{history_type_names}]+)/(?P<model_id>[0-9]+)/history', audit_history.ViewSet, basename='_api_centurionaudit_sub')
router.register('core/history', audit_history.NoDocsViewSet, basename='_api_centurionaudit')

router.register('(?P<app_label>[a-z_]+)/(?P<model_name>.+)/(?P<model_id>[0-9]+)/history', history_v2.ViewSet, basename='_api_v2_model_history')


ticket_type_names = str(ticket_type_names)[:-1]

router.register(f'core/ticket/(?P<ticket_model>[{ticket_type_names}]+)', ticket.ViewSet, feature_flag = '2025-00006', basename='_api_v2_ticket_sub')
router.register('core/ticket', ticket.NoDocsViewSet, basename='_api_v2_ticket')


router.register('core/ticket/(?P<ticket_id>[0-9]+)/comment', ticket_comment.NoDocsViewSet, feature_flag = '2025-00006', basename='_api_v2_ticket_comment_base')
router.register('core/ticket/(?P<ticket_id>[0-9]+)/comment/(?P<parent_id>[0-9]+)/threads', ticket_comment.ViewSet, feature_flag = '2025-00006', basename='_api_v2_ticket_comment_base_thread')



router.register('core/ticket/(?P<ticket_id>[0-9]+)/comments', ticket_comment_depreciated.ViewSet, basename='_api_v2_ticket_comment')
router.register('core/ticket/(?P<ticket_id>[0-9]+)/comments/(?P<parent_id>[0-9]+)/threads', ticket_comment_depreciated.ViewSet, basename='_api_v2_ticket_comment_threads')
router.register('core/ticket/(?P<ticket_id>[0-9]+)/linked_item', ticket_linked_item.ViewSet, basename='_api_v2_ticket_linked_item')
router.register('core/ticket/(?P<ticket_id>[0-9]+)/related_ticket', related_ticket.ViewSet, basename='_api_v2_ticket_related')


ticket_comment_names = str(ticket_comment_names)[:-1]

router.register(f'core/ticket/(?P<ticket_id>[0-9]+)/(?P<ticket_comment_model>[{ticket_comment_names}]+)', ticket_comment.ViewSet, feature_flag = '2025-00006', basename='_api_v2_ticket_comment_base_sub')
router.register(f'core/ticket/(?P<ticket_id>[0-9]+)/(?P<ticket_comment_model>[{ticket_comment_names}]+)/(?P<parent_id>[0-9]+)/threads', ticket_comment.ViewSet, feature_flag = '2025-00006', basename='_api_v2_ticket_comment_base_sub_thread')


router.register('core/(?P<item_class>[a-z_]+)/(?P<item_id>[0-9]+)/item_ticket', ticket_linked_item.ViewSet, basename='_api_v2_item_tickets')


router.register('itam', itam_index_v2.Index, basename='_api_v2_itam_home')

from accounting.viewsets import asset
router.register('itam/(?P<asset_model>[it_asset]+)', asset.ViewSet, feature_flag = '2025-00007', basename='_api_v2_itam_asset')

router.register('itam/device', device_v2.ViewSet, basename='_api_v2_device')
router.register('itam/device/(?P<device_id>[0-9]+)/operating_system', device_operating_system.ViewSet, basename='_api_v2_device_operating_system')
router.register('itam/device/(?P<device_id>[0-9]+)/software', device_software_v2.ViewSet, basename='_api_v2_device_software')
router.register('itam/device/(?P<device_id>[0-9]+)/service', service_device_v2.ViewSet, basename='_api_v2_service_device')
router.register('itam/device/(?P<model_id>[0-9]+)/notes', device_notes.ViewSet, basename='_api_v2_device_note')
router.register('itam/inventory', inventory.ViewSet, basename='_api_v2_inventory')
router.register('itam/operating_system', operating_system_v2.ViewSet, basename='_api_v2_operating_system')
router.register('itam/operating_system/(?P<operating_system_id>[0-9]+)/installs', device_operating_system.ViewSet, basename='_api_v2_operating_system_installs')
router.register('itam/operating_system/(?P<model_id>[0-9]+)/notes', operating_system_notes.ViewSet, basename='_api_v2_operating_system_note')
router.register('itam/operating_system/(?P<operating_system_id>[0-9]+)/version', operating_system_version_v2.ViewSet, basename='_api_v2_operating_system_version')
router.register('itam/operating_system/(?P<operating_system_id>[0-9]+)/version/(?P<model_id>[0-9]+)/notes', operating_system_version_notes.ViewSet, basename='_api_v2_operating_system_version_note')
router.register('itam/software', software_v2.ViewSet, basename='_api_v2_software')
router.register('itam/software/(?P<software_id>[0-9]+)/installs', device_software_v2.ViewSet, basename='_api_v2_software_installs')
router.register('itam/software/(?P<model_id>[0-9]+)/notes', software_notes.ViewSet, basename='_api_v2_software_note')
router.register('itam/software/(?P<software_id>[0-9]+)/version', software_version_v2.ViewSet, basename='_api_v2_software_version')
router.register('itam/software/(?P<software_id>[0-9]+)/version/(?P<model_id>[0-9]+)/notes', software_version_notes.ViewSet, basename='_api_v2_software_version_note')
router.register('itam/software/(?P<software_id>[0-9]+)/feature_flag', software_enable_feature_flag.ViewSet, basename='_api_v2_feature_flag_software')


router.register('itim', itim_v2.Index, basename='_api_v2_itim_home')
router.register('itim/ticket/change', change.ViewSet, basename='_api_v2_ticket_change')
router.register('itim/cluster', cluster_v2.ViewSet, basename='_api_v2_cluster')
router.register('itim/cluster/(?P<cluster_id>[0-9]+)/service', service_cluster.ViewSet, basename='_api_v2_service_cluster')
router.register('itim/cluster/(?P<model_id>[0-9]+)/notes', cluster_notes.ViewSet, basename='_api_v2_cluster_note')
router.register('itim/ticket/incident', incident.ViewSet, basename='_api_v2_ticket_incident')
router.register('itim/ticket/problem', problem.ViewSet, basename='_api_v2_ticket_problem')
router.register('itim/service', service_v2.ViewSet, basename='_api_v2_service')
router.register('itim/service/(?P<model_id>[0-9]+)/notes', service_notes.ViewSet, basename='_api_v2_service_note')


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
    path("access/", include("access.urls_api")),
    path("accounting/", include("accounting.urls")),
    path("devops/", include("devops.urls")),
    path("hr/", include('human_resources.urls')),
    path('public/', include('api.urls_public')),
]
