import pytest

from django.db import models
from django.test import Client

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_externallink
class ExternalLinkAPITestCases(
    APIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            'name': {
                'expected': str
            },
            'button_text': {
                'expected': str
            },
            'template': {
                'expected': str
            },
            'colour': {
                'expected': str
            },
            'cluster': {
                'expected': bool
            },
            'devices': {
                'expected': bool
            },
            'service': {
                'expected': bool
            },
            'software': {
                'expected': bool
            },
            'modified': {
                'expected': str
            }
        }



class ExternalLinkAPIInheritedCases(
    ExternalLinkAPITestCases,
):
    pass



@pytest.mark.module_settings
class ExternalLinkAPIPyTest(
    ExternalLinkAPITestCases,
):

    pass
