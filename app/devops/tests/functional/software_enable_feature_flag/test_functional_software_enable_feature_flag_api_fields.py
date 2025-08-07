import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_featureflag
class SoftwareEnableFeatureFlagAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'software': {
                'expected': dict
            },
            'software.id': {
                'expected': int
            },
            'software.display_name': {
                'expected': str
            },
            'software.url': {
                'expected': Hyperlink
            },
            'name': {
                'expected': str
            },
            'description': {
                'expected': str
            },
            'enabled': {
                'expected': bool
            },
            'modified': {
                'expected': str
            }
        }



class SoftwareEnableFeatureFlagAPIInheritedCases(
    SoftwareEnableFeatureFlagAPITestCases,
):
    pass



@pytest.mark.module_devops
class SoftwareEnableFeatureFlagAPIPyTest(
    SoftwareEnableFeatureFlagAPITestCases,
):

    pass
