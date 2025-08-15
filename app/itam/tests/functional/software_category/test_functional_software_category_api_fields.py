import pytest

# from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_softwarecategory
class SoftwareCategoryAPITestCases(
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



class SoftwareCategoryAPIInheritedCases(
    SoftwareCategoryAPITestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareCategoryAPIPyTest(
    SoftwareCategoryAPITestCases,
):

    pass
