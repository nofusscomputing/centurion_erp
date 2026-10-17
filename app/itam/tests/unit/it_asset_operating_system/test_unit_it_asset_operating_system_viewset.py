import pytest

from itam.models import ITAssetOperatingSystem
from itam.tests.unit.itam_asset_base.test_unit_itam_asset_base_viewset import (
    AssetBase,
    ITAMAssetBaseViewsetInheritedCases,
    NoDocsViewSet,
    ViewSet
)



@pytest.mark.model_itassetoperatingsystem
class ITAssetOperatingSystemBaseViewsetTestCases(
    ITAMAssetBaseViewsetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            # '_log': {
            #     'type': logging.Logger,
            #     'value': None
            # },
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
                'value': None
            },
            'base_model': {
                'value': AssetBase
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'asset_number',
                    'serial_number',
                    'organization',
                ]
            },
            'model': {
                'value': ITAssetOperatingSystem
            },
            'model_documentation': {
                'type': type(None),
                'value': None
            },
            'model_kwarg': {
                'value': 'model_name'
            },
            'model_suffix': {
                'type': type(None)
            },
            'queryset': {
                'type': type(None),
                'value': None
            },
            'serializer_class': {
                'type': type(None),
                'value': None
            },
            'search_fields': {
                'value': [
                    'asset_number',
                    'serial_number',
                ]
            },
            'view_description': {
                'value': 'All Assets'
            },
            'view_name': {
                'type': type(None),
                'value': None
            },
            'view_serializer_name': {
                'type': type(None),
                'value': None
            }
        }



class ITAssetOperatingSystemViewsetInheritedCases(
    ITAssetOperatingSystemBaseViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetOperatingSystemViewsetPyTest(
    ITAssetOperatingSystemBaseViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet
