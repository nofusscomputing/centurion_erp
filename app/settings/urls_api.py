from assistance.viewsets import (
    knowledge_base_category as knowledge_base_category_v2,
)

from api.viewsets import (
    auth_token,
)

from centurion_feature_flag.urls.routers import DefaultRouter

from core.viewsets import (
    celery_log as celery_log_v2,
    manufacturer as manufacturer_v2,
    ticket_category,
    ticket_comment_category,

)

from itam.viewsets import (
    device_model,
    device_type,
    software_category as software_category_v2,
)

from itim.viewsets import (
    cluster_type as cluster_type_v2,
    port as port_v2,
)

from project_management.viewsets import (
    project_state,
    project_type,
)

from settings.viewsets import (
    app_settings,
    external_link as external_link_v2,
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
    prefix = 'app_settings', viewset = app_settings.ViewSet,
    basename = '_api_appsettings'
)
router.register(
    prefix = 'celery_log', viewset = celery_log_v2.ViewSet,
    basename = '_api_v2_celery_log'
)
router.register(
    prefix = 'cluster_type', viewset = cluster_type_v2.ViewSet,
    basename = '_api_clustertype'
)
router.register(
    prefix = 'device_model', viewset = device_model.ViewSet,
    basename = '_api_devicemodel'
)
router.register(
    prefix = 'device_type', viewset = device_type.ViewSet,
    basename = '_api_devicetype'
)
router.register(
    prefix = 'external_link', viewset = external_link_v2.ViewSet,
    basename = '_api_v2_external_link'
)
router.register(
    prefix = 'knowledge_base_category',
    viewset = knowledge_base_category_v2.ViewSet,
    basename = '_api_knowledgebasecategory'
)
router.register(
    prefix = 'manufacturer', viewset = manufacturer_v2.ViewSet,
    basename = '_api_manufacturer'
)
router.register(
    prefix = 'port', viewset = port_v2.ViewSet,
    basename = '_api_port'
)
router.register(
    prefix = 'project_state',
    viewset = project_state.ViewSet,
    basename = '_api_projectstate'
)
router.register(
    prefix = 'project_type', viewset = project_type.ViewSet,
    basename = '_api_projecttype'
)
router.register(
    prefix = 'software_category', viewset = software_category_v2.ViewSet,
    basename = '_api_softwarecategory'
)
router.register(
    prefix = 'ticket_category',
    viewset = ticket_category.ViewSet, basename = '_api_ticketcategory'
)
router.register(
    prefix = 'ticket_comment_category',
    viewset = ticket_comment_category.ViewSet,
    basename = '_api_ticketcommentcategory'
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
