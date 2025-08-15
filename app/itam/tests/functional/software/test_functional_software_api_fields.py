import pytest

# from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_software
class SoftwareAPITestCases(
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
                'expected': Hyperlink
            },
            'name': {
                'expected': str
            },
            'category': {
                'expected': dict
            },
            'category.id': {
                'expected': int
            },
            'category.display_name': {
                'expected': str
            },
            'category.url': {
                'expected': Hyperlink
            },
            'modified': {
                'expected': str
            }
        }



class SoftwareAPIInheritedCases(
    SoftwareAPITestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareAPIPyTest(
    SoftwareAPITestCases,
):

    pass
