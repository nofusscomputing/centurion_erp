import pytest

from django.db import models

from itim.tests.unit.ticket_slm.test_unit_ticket_slm_model import SLMTicketModelInheritedCases

from itim.models.request_ticket import RequestTicket



@pytest.mark.model_requestticket
class RequestTicketTestCases(
    SLMTicketModelInheritedCases
):

    sub_model_type = 'request'


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
            'model_tag': {
                'type': str,
                'value': 'ticket'
            },
            'url_model_name': {
                'type': str,
                'value': 'ticketbase'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}



    def test_class_inherits_requestticket(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, RequestTicket)


    def test_function_get_ticket_type(self, model):
        """Function test

        As this model is intended to be used alone.

        Ensure that function `get_ticket_type` returns `request` for model
        `RequestTicket`
        """

        assert model().get_ticket_type == 'request'



class RequestTicketInheritedCases(
    RequestTicketTestCases,
):

    sub_model_type = None



@pytest.mark.module_itim
class RequestTicketPyTest(
    RequestTicketTestCases,
):
    pass
