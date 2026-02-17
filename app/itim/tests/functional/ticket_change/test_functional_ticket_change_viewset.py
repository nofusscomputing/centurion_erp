
import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)



@pytest.mark.model_changeticket
class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):
    pass



class ChangeTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ChangeTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
