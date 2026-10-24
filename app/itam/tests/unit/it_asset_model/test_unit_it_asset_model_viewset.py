import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    ModelViewSetInheritedCases
)

from itam.models import ITAssetModel
from itam.viewsets.asset_model import (
    ViewSet,
)



@pytest.mark.model_itassetmodel
class ITAssetModelBaseViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
            },
            'filterset_fields': {
                'value': [
                    'name',
                    'manufacturer',
                    'organization',
                ]
            },
            'model': {
                'value': ITAssetModel
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name'
                ]
            },
            'view_description': {
                'type': type(None),
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class ITAssetModelViewsetInheritedCases(
    ITAssetModelBaseViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelViewsetPyTest(
    ITAssetModelBaseViewsetTestCases,
):
    pass
