import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_api_fields import (
    TicketBaseAPIInheritedCases,
)



@pytest.mark.model_changeticket
class ChangeTicketAPITestCases(
    TicketBaseAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {}



class ChangeTicketAPIInheritedCases(
    ChangeTicketAPITestCases,
):

    pass



@pytest.mark.module_itim
class ChangeTicketAPIPyTest(
    ChangeTicketAPITestCases,
):

    pass
