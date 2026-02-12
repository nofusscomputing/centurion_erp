import pytest

from itim.tests.unit.ticket_slm.test_unit_ticket_slm_model import SLMTicketModelInheritedCases

from itim.models.ticket_incident import IncidentTicket



@pytest.mark.model_incidentticket
class IncidentTicketTestCases(
    SLMTicketModelInheritedCases
):

    sub_model_type = 'incident'


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

        return {}



    def test_class_inherits_incidentticket(self, model):
        """ Class inheritence

        Model Must Inherit from requestticket
        """

        assert issubclass(model, IncidentTicket)


    def test_function_get_ticket_type(self, model):
        """Function test

        As this model is intended to be used alone.

        Ensure that function `get_ticket_type` returns `request` for model
        `IncidentTicket`
        """

        assert model().get_ticket_type == 'incident'



class IncidentTicketInheritedCases(
    IncidentTicketTestCases,
):

    sub_model_type = None



@pytest.mark.module_itim
class IncidentTicketPyTest(
    IncidentTicketTestCases,
):
    pass
