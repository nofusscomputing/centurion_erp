import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itam.viewsets.operating_system import (
    OperatingSystem,
    ViewSet,
)



@pytest.mark.model_operatingsystem
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
                'type': str,
                'value': 'itam/operating_system'
            },
            'filterset_fields': {
                'value': [
                    'organization',
                    'publisher'
                ]
            },
            'model': {
                'value': OperatingSystem
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
                'value': 'Operating Systems'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class OperatingSystemViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemViewsetPyTest(
    ViewsetTestCases,
):

    pass
