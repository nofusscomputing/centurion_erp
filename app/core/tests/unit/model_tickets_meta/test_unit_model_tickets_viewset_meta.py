import pytest

from core.viewsets.ticket_model_link import (
    ModelTicket,
    ViewSet,
)

from core.tests.unit.model_tickets.test_unit_model_tickets_viewset import (
    ModelTicketViewsetInheritedCases
)


@pytest.mark.tickets
@pytest.mark.model_modelticket
class ViewsetTestCases(
        ModelTicketViewsetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_model_documentation': {
                'type': type(None),
                'value': None
            },
            'back_url': {
                'type': type(None),
            },
            'base_model': {
                'value': ModelTicket
            },
            'documentation': {
                'type': type(None),
            },
            'filterset_fields': {
                'value': [
                   'ticket',
                   'organization'
                ]
            },
            'model': {
                'value': ModelTicket
            },
            'model_documentation': {
                'type': type(None),
            },
            'model_kwarg': {
                'value': 'model_name'
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': []
            },
            'view_description': {
                'value': 'Models linked to ticket'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class ModelTicketViewsetMetaInheritedCases(
    ViewsetTestCases,
):
    pass
