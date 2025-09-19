import pytest

from itim.tests.functional.ticket_slm.test_functional_ticket_slm_api_fields import TicketSLMAPIInheritedCases



@pytest.mark.model_requestticket
class TicketRequestAPITestCases(
    TicketSLMAPIInheritedCases,
):

    pass



class TicketRequestAPIInheritedCases(
    TicketRequestAPITestCases,
):

    pass



@pytest.mark.module_itim
class TicketRequestAPIPyTest(
    TicketRequestAPITestCases,
):

    pass
