import pytest

from accounting.viewsets.asset import (
    NoDocsViewSet,
    AssetBase,
    ViewSet,
)

from api.tests.unit.viewset.test_unit_tenancy_viewset import SubModelViewSetInheritedCases



@pytest.mark.model_assetbase
class AssetBaseViewsetTestCases(
    SubModelViewSetInheritedCases,
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
                'value': AssetBase
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



class AssetBaseViewsetInheritedCases(
    AssetBaseViewsetTestCases,
):
    pass



@pytest.mark.module_access
class AssetBaseViewsetPyTest(
    AssetBaseViewsetTestCases,
):

    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return NoDocsViewSet
