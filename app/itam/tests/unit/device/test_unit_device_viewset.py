import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itam.viewsets.device import (
    Device,
    ViewSet,
)



@pytest.mark.model_device
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
                    'serial_number',
                    'organization',
                    'uuid',
                    'cluster_device',
                    'cluster_node'
                ]
            },
            'model': {
                'value': Device
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name',
                    'serial_number',
                    'uuid'
                ]
            },
            'view_description': {
                'value': 'Physical Devices'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class DeviceViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class DeviceViewsetPyTest(
    ViewsetTestCases,
):

    pass
