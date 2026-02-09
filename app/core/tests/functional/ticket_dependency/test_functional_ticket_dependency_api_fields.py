import pytest

from django.db import models

from api.tests.functional.test_functional_api_fields import (
    APIFieldsInheritedCases,
)



@pytest.mark.model_tickets
@pytest.mark.model_ticketdependency
class TicketDependencyAPITestCases(
    APIFieldsInheritedCases,
):


    @property
    def parameterized_api_fields(self):

        return {
            '_urls.notes': {
                'expected': models.NOT_PROVIDED
            },
            'display_name': {
                'expected': dict
            },
            'display_name.markdown': {
                'expected': str
            },
            'display_name.render': {
                'expected' :dict
            },
            'model_notes': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.markdown': {
                'expected': models.NOT_PROVIDED
            },
            'model_notes.render': {
                'expected': models.NOT_PROVIDED
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
            'how_related': {
                'expected': int
            },
            'dependent_ticket': {
                'expected': dict
            },
            'dependent_ticket.id': {
                'expected': int
            },
            'dependent_ticket.display_name': {
                'expected': str
            },
            'dependent_ticket.url': {
                'expected': str
            },
            'created': {
                'expected': models.NOT_PROVIDED
            },
            'modified': {
                'expected': models.NOT_PROVIDED
            },
        }


    @property
    def parameterized_api_metadata_fields(self) -> dict:

        return {
            # 'table_fields': {
            #     'expected': models.NOT_PROVIDED
            # },
        }



class TicketDependencyAPIInheritedCases(
    TicketDependencyAPITestCases,
):
    pass


@pytest.mark.module_core
class TicketDependencyAPIPyTest(
    TicketDependencyAPITestCases,
):

    pass
