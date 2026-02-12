import pytest

from itim.tests.functional.ticket_slm.test_functional_ticket_slm_viewset import (
    SLMTicketViewsetInheritedCases
)



@pytest.mark.model_incidentticket
class ViewsetTestCases(
    SLMTicketViewsetInheritedCases,
):
    pass



class IncidentTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class IncidentTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
