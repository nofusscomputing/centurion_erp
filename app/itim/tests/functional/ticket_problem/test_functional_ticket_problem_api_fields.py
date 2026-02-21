import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_api_fields import (
    TicketBaseAPIInheritedCases,
)



@pytest.mark.model_problemticket
class ProblemTicketAPITestCases(
    TicketBaseAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'business_impact': {
                'expected': str
            },
            'cause_analysis': {
                'expected': str
            },
            'observations': {
                'expected': str
            },
            'workaround': {
                'expected': str
            },
        }



class ProblemTicketAPIInheritedCases(
    ProblemTicketAPITestCases,
):

    pass



@pytest.mark.module_itim
class ProblemTicketAPIPyTest(
    ProblemTicketAPITestCases,
):

    pass
