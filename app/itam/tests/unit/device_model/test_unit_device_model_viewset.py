import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itam.viewsets.device_model import (
    DeviceModel,
    ViewSet,
)



@pytest.mark.model_devicemodel
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
                    'name',
                    'manufacturer',
                    'organization'
                ]
            },
            'model': {
                'value': DeviceModel
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
                'value': 'Device Models'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class DeviceModelViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceModelViewsetPyTest(
    ViewsetTestCases,
):

    pass
