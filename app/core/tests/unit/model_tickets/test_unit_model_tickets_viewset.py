import pytest

from core.viewsets.ticket_model_link import (
    ModelTicket,
    ViewSet,
)

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    SubModelViewSetInheritedCases,
)



@pytest.mark.tickets
@pytest.mark.model_modelticket
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
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
            'model_suffix': {
                'type': str,
                'value': 'ticket'
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



class ModelTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class ModelTicketViewsetPyTest(
    ViewsetTestCases,
):
    pass
