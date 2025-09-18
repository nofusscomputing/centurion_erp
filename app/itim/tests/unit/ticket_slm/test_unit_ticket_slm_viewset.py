import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)
from core.viewsets.ticket import (
    TicketBase,
    ViewSet,
)

from itim.models.slm_ticket_base import (
    SLMTicket
)



@pytest.mark.model_slmticket
class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            'base_model': {
                'value': TicketBase,
            },
            'model': {
                'value': SLMTicket
            },
        }



class SLMTicketBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class SLMTicketBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
