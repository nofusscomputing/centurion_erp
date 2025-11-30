import pytest

from django.db import models

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    SubModelViewSetInheritedCases,
)

from core.models.ticket_base import TicketBase
from core.viewsets.ticket_model_link import (
    ModelTicket,
    ViewSet,
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
            'metadata_markdown': {
                'value': True
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
            'parent_model': {
                'type': models.base.ModelBase,
                'value': TicketBase
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'model_id'
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



    def test_function_get_parent_model(self, viewset):

        assert viewset().get_parent_model() is TicketBase



class ModelTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class ModelTicketViewsetPyTest(
    ViewsetTestCases,
):
    pass
