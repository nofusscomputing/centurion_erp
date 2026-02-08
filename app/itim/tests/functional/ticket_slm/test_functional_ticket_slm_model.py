import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_model import (
    TicketBaseModelInheritedTestCases
)



@pytest.mark.model_slmticket
class SLMTicketModelTestCases(
    TicketBaseModelInheritedTestCases
):

    @property
    def parameterized_model_fields(self):

        return {
            'ttr': {
                'field': 'ttr',
                'type': int
            },
            'tto': {
                'field': 'tto',
                'type': int
            },
        }



class SLMTicketModelInheritedTestCases(
    SLMTicketModelTestCases
):

    pass


@pytest.mark.module_itim
class SLMTicketModelPyTest(
    SLMTicketModelTestCases
):

    pass
