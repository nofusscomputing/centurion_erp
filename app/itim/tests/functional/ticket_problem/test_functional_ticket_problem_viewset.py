
import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)



@pytest.mark.model_problemticket
class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):
    pass



class ProblemTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ProblemTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
