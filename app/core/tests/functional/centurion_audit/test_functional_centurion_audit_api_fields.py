import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_centurionaudit
class CenturionAuditAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            'modified': {
                'expected': models.NOT_PROVIDED
            },
            'content_type': {
                'expected': dict
            },
            'content_type.id': {
                'expected': int
            },
            'content_type.display_name': {
                'expected': str
            },
            'content_type.url': {
                'expected': Hyperlink
            },
            'before': {
                'expected': dict
            },
            'after': {
                'expected': dict
            },
            'action': {
                'expected': int
            },
            'user': {
                'expected': dict
            },
            'user.id': {
                'expected': int
            },
            'user.display_name': {
                'expected': str
            },
            'user.url': {
                'expected': Hyperlink
            },
        }



class CenturionAuditAPIInheritedCases(
    CenturionAuditAPITestCases,
):
    pass



@pytest.mark.module_core
class CenturionAuditAPIPyTest(
    CenturionAuditAPITestCases,
):

    pass
