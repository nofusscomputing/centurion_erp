import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)
from core.viewsets.ticket import (
    ViewSet,
)

from itim.models.ticket_change import (
    ChangeTicket
)



@pytest.mark.model_changeticket
class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': ChangeTicket
            },
        }



class ChangeTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ChangeTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
