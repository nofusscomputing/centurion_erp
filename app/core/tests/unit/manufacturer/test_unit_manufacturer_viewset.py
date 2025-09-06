
import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from core.viewsets.manufacturer import (
    Manufacturer,
    ViewSet,
)



@pytest.mark.model_manufacturer
class ViewsetTestCases(
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
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'organization'
                ]
            },
            'model': {
                'value': Manufacturer
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
                'value': 'Manufacturer(s) / Publishers'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class ManufacturerViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class ManufacturerViewsetPyTest(
    ViewsetTestCases,
):

    pass
