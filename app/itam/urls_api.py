from centurion_feature_flag.urls.routers import DefaultRouter

from accounting.viewsets import asset

from devops.viewsets import (
    software_enable_feature_flag,
)

from itam.viewsets import (
    index as itam_index_v2,
    device,
    device_software as device_software_v2,
    device_operating_system,
    inventory,
    operating_system as operating_system_v2,
    operating_system_version as operating_system_version_v2,
    software as software_v2,
    software_version as software_version_v2,
)

from itim.viewsets import (
    service_device as service_device_v2,
)


# app_name = "itam"


router: DefaultRouter = DefaultRouter(trailing_slash=False)


router.register(
    prefix = '', viewset = itam_index_v2.Index,
    basename = '_api_v2_itam_home'
)
router.register(
    prefix = '(?P<asset_model>[it_asset]+)', viewset = asset.ViewSet,
    feature_flag = '2025-00007', basename = '_api_v2_itam_asset'
)
router.register(
    prefix = 'device', viewset = device.ViewSet,
    basename = '_api_device'
)
router.register(
    prefix = 'device/(?P<device_id>[0-9]+)/operating_system',
    viewset = device_operating_system.ViewSet,
    basename = '_api_deviceoperatingsystem')
router.register(
    prefix = 'device/(?P<device_id>[0-9]+)/software', viewset = device_software_v2.ViewSet,
    basename = '_api_devicesoftware'
)
router.register(
    prefix = 'device/(?P<device_id>[0-9]+)/service', viewset = service_device_v2.ViewSet,
    basename = '_api_v2_service_device'
)
router.register(
    prefix = 'inventory', viewset = inventory.ViewSet,
    basename = '_api_v2_inventory'
)
router.register(
    prefix = 'operating_system', viewset = operating_system_v2.ViewSet,
    basename = '_api_operatingsystem'
)
router.register(
    prefix = 'operating_system/(?P<operating_system_id>[0-9]+)/installs',
    viewset = device_operating_system.ViewSet,
    basename = '_api_v2_operating_system_installs'
)
router.register(
    prefix = 'operating_system/(?P<operating_system_id>[0-9]+)/version',
    viewset = operating_system_version_v2.ViewSet,
    basename = '_api_operatingsystemversion'
)
router.register(
    prefix = 'software', viewset = software_v2.ViewSet,
    basename = '_api_software'
)
router.register(
    prefix = 'software/(?P<software_id>[0-9]+)/installs', viewset = device_software_v2.ViewSet,
    basename = '_api_v2_software_installs'
)
router.register(
    prefix = 'software/(?P<software_id>[0-9]+)/version', viewset = software_version_v2.ViewSet,
    basename = '_api_v2_software_version'
)
router.register(
    prefix = 'software/(?P<software_id>[0-9]+)/feature_flag',
    viewset = software_enable_feature_flag.ViewSet,
    basename = '_api_softwareenablefeatureflag'
)


urlpatterns = router.urls
