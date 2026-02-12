import pytest

from itim.tests.functional.ticket_slm.test_functional_ticket_slm_api_fields import TicketSLMAPIInheritedCases



@pytest.mark.model_incidentticket
class IncidentTicketAPITestCases(
    TicketSLMAPIInheritedCases,
):

    pass



class IncidentTicketAPIInheritedCases(
    IncidentTicketAPITestCases,
):

    pass



@pytest.mark.module_itim
class IncidentTicketAPIPyTest(
    IncidentTicketAPITestCases,
):

    pass
