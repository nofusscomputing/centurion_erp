import pytest

# from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_operatingsystem
class OperatingSystemAPITestCases(
    APIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'publisher': {
                'expected': dict
            },
            'publisher.id': {
                'expected': int
            },
            'publisher.display_name': {
                'expected': str
            },
            'publisher.url': {
                'expected': str
            },
            'name': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class OperatingSystemAPIInheritedCases(
    OperatingSystemAPITestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemAPIPyTest(
    OperatingSystemAPITestCases,
):

    pass
