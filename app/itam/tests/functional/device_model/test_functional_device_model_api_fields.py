import pytest

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_device
class DeviceModelAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            'manufacturer': {
                'expected': dict
            },
            'manufacturer.id': {
                'expected': int
            },
            'manufacturer.display_name': {
                'expected': str
            },
            'manufacturer.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class DeviceModelAPIInheritedCases(
    DeviceModelAPITestCases,
):
    pass



@pytest.mark.module_itam
class DeviceModelAPIPyTest(
    DeviceModelAPITestCases,
):

    pass
