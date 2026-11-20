import pytest

from itim.tests.unit.ticket_slm.test_unit_ticket_slm_viewset import (
    SLMTicketBaseViewsetInheritedCases
)



@pytest.mark.model_incidentticket
class IncidentTicketViewSetTestCases(
    SLMTicketBaseViewsetInheritedCases
):
    pass



class IncidentTicketViewSetInheritedCases(
    IncidentTicketViewSetTestCases
):
    pass



@pytest.mark.module_itim
class IncidentTicketViewSetPyTest(
    IncidentTicketViewSetTestCases
):
    pass