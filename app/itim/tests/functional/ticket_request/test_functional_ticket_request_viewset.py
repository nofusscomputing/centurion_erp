import pytest

from itim.tests.functional.ticket_slm.test_functional_ticket_slm_viewset import (
    SLMTicketViewsetInheritedCases
)



@pytest.mark.model_requestticket
class ViewsetTestCases(
    SLMTicketViewsetInheritedCases,
):
    pass



class RequestTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class RequestTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
