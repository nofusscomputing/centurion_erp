import pytest

from django.db import models

from core.tests.unit.ticket_base.test_unit_ticket_base_model import TicketBaseModelInheritedCases

from itim.models.slm_ticket_base import SLMTicket



@pytest.mark.model_slmticket
class SLMTicketModelTestCases(
    TicketBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_notes_enabled': {
                'value': False
            },
            '_is_submodel': {
                'value': True
            },
            'url_model_name': {
                'type': str,
                'value': 'ticketbase'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            "tto": {
                'blank': True,
                'default': 0,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
            "ttr": {
                'blank': True,
                'default': 0,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
        }



    def test_class_inherits_SLMTicket(self, model):
        """ Class inheritence

        Model Must Inherit from slmticket
        """

        assert issubclass(model, SLMTicket)



class SLMTicketModelInheritedCases(
    SLMTicketModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_itim
class SLMTicketModelPyTest(
    SLMTicketModelTestCases,
):

    sub_model_type = 'slm'
