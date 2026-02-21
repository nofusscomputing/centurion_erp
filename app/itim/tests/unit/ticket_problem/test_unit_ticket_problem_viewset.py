import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)
from core.viewsets.ticket import (
    TicketBase,
    ViewSet,
)

from itim.models.ticket_problem import (
    ProblemTicket
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
                'value': ProblemTicket
            },
        }



class ProblemTicketBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ProblemTicketBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
