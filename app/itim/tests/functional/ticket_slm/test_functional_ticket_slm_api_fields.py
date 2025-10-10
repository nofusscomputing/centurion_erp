import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_api_fields import (
    TicketBaseAPIInheritedCases,
)



@pytest.mark.model_slmticket
class TicketSLMAPITestCases(
    TicketBaseAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {
            'tto': {
                'expected': int
            },
            'ttr': {
                'expected': int
            }
        }



class TicketSLMAPIInheritedCases(
    TicketSLMAPITestCases,
):

    pass


#
# This is a base model and does not have api access
#
# class TicketSLMAPIPyTest(
#     TicketRequestAPITestCases,
# ):

#     pass
