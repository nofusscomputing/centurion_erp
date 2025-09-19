
import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)



@pytest.mark.model_slmticket
class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):
    pass



class SLMTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class SLMTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
