from centurion_feature_flag.urls.routers import DefaultRouter

from config_management.viewsets import (
    index as config_management_v2,
    config_group as config_group_v2,
    config_group_software as config_group_software_v2
)



# app_name = "config_management"

router: DefaultRouter = DefaultRouter(trailing_slash=False)


router.register(
    prefix = '', viewset = config_management_v2.Index,
    basename = '_api_v2_config_management_home'
)
router.register(
    prefix = '/group', viewset = config_group_v2.ViewSet,
    basename = '_api_configgroups'
)
router.register(
    prefix = '/group/(?P<parent_group>[0-9]+)/child_group', viewset = config_group_v2.ViewSet,
    basename = '_api_configgroups_child'
)
router.register(
    prefix = '/group/(?P<config_group_id>[0-9]+)/software',
    viewset = config_group_software_v2.ViewSet,
    basename = '_api_configgroupsoftware'
)


urlpatterns = router.urls
