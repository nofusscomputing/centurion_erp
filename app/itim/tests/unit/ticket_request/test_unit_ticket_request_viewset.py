import pytest

from itim.models.request_ticket import RequestTicket
from itim.tests.unit.ticket_slm.test_unit_ticket_slm_viewset import (
    SLMTicketBaseViewsetInheritedCases
)



@pytest.mark.model_requestticket
class RequestTicketViewSetTestCases(
    SLMTicketBaseViewsetInheritedCases
):

    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': RequestTicket
            },
        }




class RequestTicketViewSetInheritedCases(
    RequestTicketViewSetTestCases
):
    pass



@pytest.mark.module_itim
class RequestTicketViewSetPyTest(
    RequestTicketViewSetTestCases
):
    pass