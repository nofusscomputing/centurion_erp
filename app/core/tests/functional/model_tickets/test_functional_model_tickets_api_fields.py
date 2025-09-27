import pytest

from django.db import models

from rest_framework.relations import Hyperlink

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.tickets
@pytest.mark.model_modelticket
class ModelTicketAPITestCases(
    APIFieldsInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            '_urls.notes': {
                'expected': models.NOT_PROVIDED,
                'type': models.NOT_PROVIDED,
            },
            'model_notes': {
                'expected': models.NOT_PROVIDED,
                'type': models.NOT_PROVIDED,
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
            'ticket': {
                'expected': dict
            },
            'ticket.id': {
                'expected': int
            },
            'ticket.display_name': {
                'expected': str
            },
            'ticket.url': {
                'expected': str
            },
            'modified': {
                'expected': str
            }
        }



class ModelTicketAPIInheritedCases(
    ModelTicketAPITestCases,
):
    pass



@pytest.mark.module_core
class ModelTicketAPIPyTest(
    ModelTicketAPITestCases,
):

    pass
