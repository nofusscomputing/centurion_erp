from core.tests.unit.ticket_base.test_unit_ticket_base_api_fields import (
    TicketBaseAPIInheritedCases,
)



class TicketSLMAPITestCases(
    TicketBaseAPIInheritedCases,
):

    parameterized_test_data = {
        'tto': {
            'expected': int
        },
        'ttr': {
            'expected': int
        }
    }

    kwargs_create_item: dict = {
        'tto': 11,
        'ttr': 22,
    }



class TicketSLMAPIInheritedCases(
    TicketSLMAPITestCases,
):

    kwargs_create_item: dict = None

    model = None


#
# This is a base model and does not have api access
#
# class TicketSLMAPIPyTest(
#     TicketRequestAPITestCases,
# ):

#     pass
