import pytest

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_devicetype
class DeviceTypeAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class DeviceTypeAPIInheritedCases(
    DeviceTypeAPITestCases,
):
    pass



@pytest.mark.module_itam
class DeviceTypeAPIPyTest(
    DeviceTypeAPITestCases,
):

    pass
