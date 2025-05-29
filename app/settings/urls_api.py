from assistance.viewsets import (
    knowledge_base_category as knowledge_base_category_v2,
    knowledge_base_category_notes,
)

from api.viewsets import (
    auth_token,
)

from centurion_feature_flag.urls.routers import DefaultRouter

from core.viewsets import (
    celery_log as celery_log_v2,
    manufacturer as manufacturer_v2,
    manufacturer_notes,
    ticket_category,
    ticket_category_notes,
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
    project_state as project_state_v2,
    project_state_notes,
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



# app_name = "settings"


router: DefaultRouter = DefaultRouter(trailing_slash=False)


router.register(
    prefix = '', viewset = settings_index_v2.Index,
    basename = '_api_v2_settings_home'
)
router.register(
    prefix = 'app_settings', viewset = app_settings_v2.ViewSet,
    basename = '_api_v2_app_settings'
)
router.register(
    prefix = 'celery_log', viewset = celery_log_v2.ViewSet,
    basename = '_api_v2_celery_log'
)
router.register(
    prefix = 'cluster_type', viewset = cluster_type_v2.ViewSet,
    basename = '_api_v2_cluster_type'
)
router.register(
    prefix = 'cluster_type/(?P<model_id>[0-9]+)/notes',
    viewset = cluster_type_notes.ViewSet,
    basename = '_api_v2_cluster_type_note'
)
router.register(
    prefix = 'device_model', viewset = device_model_v2.ViewSet,
    basename = '_api_v2_device_model'
)
router.register(
    prefix = 'device_model/(?P<model_id>[0-9]+)/notes',
    viewset = device_model_notes.ViewSet,
    basename = '_api_v2_device_model_note'
)
router.register(
    prefix = 'device_type', viewset = device_type_v2.ViewSet,
    basename = '_api_v2_device_type'
)
router.register(
    prefix = 'device_type/(?P<model_id>[0-9]+)/notes',
    viewset = device_type_notes.ViewSet,
    basename = '_api_v2_device_type_note'
)
router.register(
    prefix = 'external_link', viewset = external_link_v2.ViewSet,
    basename = '_api_v2_external_link'
)
router.register(
    prefix = 'external_link/(?P<model_id>[0-9]+)/notes',
    viewset = external_link_notes.ViewSet,
    basename = '_api_v2_external_link_note'
)
router.register(
    prefix = 'knowledge_base_category',
    viewset = knowledge_base_category_v2.ViewSet,
    basename = '_api_v2_knowledge_base_category'
)
router.register(
    prefix = 'knowledge_base_category/(?P<model_id>[0-9]+)/notes',
    viewset = knowledge_base_category_notes.ViewSet,
    basename = '_api_v2_knowledge_base_category_note'
)
router.register(
    prefix = 'manufacturer', viewset = manufacturer_v2.ViewSet,
    basename = '_api_v2_manufacturer'
)
router.register(
    prefix = 'manufacturer/(?P<model_id>[0-9]+)/notes',
    viewset = manufacturer_notes.ViewSet,
    basename = '_api_v2_manufacturer_note'
)
router.register(
    prefix = 'port', viewset = port_v2.ViewSet,
    basename = '_api_v2_port'
)
router.register(
    prefix = 'port/(?P<model_id>[0-9]+)/notes', viewset = port_notes.ViewSet,
    basename = '_api_v2_port_note'
)
router.register(
    prefix = 'project_state',
    viewset = project_state_v2.ViewSet,
    basename = '_api_v2_project_state'
)
router.register(
    prefix = 'project_state/(?P<model_id>[0-9]+)/notes',
    viewset = project_state_notes.ViewSet,
    basename = '_api_v2_project_state_note'
)
router.register(
    prefix = 'project_type', viewset = project_type_v2.ViewSet,
    basename = '_api_v2_project_type'
)
router.register(
    prefix = 'project_type/(?P<model_id>[0-9]+)/notes',
    viewset = project_type_notes.ViewSet,
    basename = '_api_v2_project_type_note'
)
router.register(
    prefix = 'software_category', viewset = software_category_v2.ViewSet,
    basename = '_api_v2_software_category'
)
router.register(
    prefix = 'software_category/(?P<model_id>[0-9]+)/notes',
    viewset = software_category_notes.ViewSet,
    basename = '_api_v2_software_category_note'
)
router.register(
    prefix = 'ticket_category',
    viewset = ticket_category.ViewSet, basename = '_api_v2_ticket_category'
)
router.register(
    prefix = 'ticket_category/(?P<model_id>[0-9]+)/notes',
    viewset = ticket_category_notes.ViewSet,
    basename = '_api_v2_ticket_category_note'
)
router.register(
    prefix = 'ticket_comment_category',
    viewset = ticket_comment_category.ViewSet,
    basename = '_api_v2_ticket_comment_category'
)
router.register(
    prefix = 'ticket_comment_category/(?P<model_id>[0-9]+)/notes',
    viewset = ticket_comment_category_notes.ViewSet,
    basename = '_api_v2_ticket_comment_category_note'
)
router.register(
    prefix = 'user_settings', viewset = user_settings_v2.ViewSet,
    basename = '_api_v2_user_settings'
)
router.register(
    prefix = 'user_(?P<model_id>[0-9]+)/token', viewset = auth_token.ViewSet,
    basename = '_api_v2_user_settings_token'
)


urlpatterns = router.urls
