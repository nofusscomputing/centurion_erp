import pytest

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_operatingsystem
class OperatingSystemVersionAPITestCases(
    APIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'operating_system': {
                'expected': dict
            },
            'operating_system.id': {
                'expected': int
            },
            'operating_system.display_name': {
                'expected': str
            },
            'operating_system.url': {
                'expected': Hyperlink
            },
            'name': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class OperatingSystemVersionAPIInheritedCases(
    OperatingSystemVersionAPITestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemVersionAPIPyTest(
    OperatingSystemVersionAPITestCases,
):

    pass
