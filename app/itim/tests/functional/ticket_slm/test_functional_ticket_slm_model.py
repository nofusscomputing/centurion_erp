import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_model import (
    TicketBaseModelInheritedTestCases
)



@pytest.mark.model_slmticket
class SLMTicketModelTestCases(
    TicketBaseModelInheritedTestCases
):
    pass


class SLMTicketModelInheritedTestCases(
    SLMTicketModelTestCases
):

    pass


@pytest.mark.module_itim
class SLMTicketModelPyTest(
    SLMTicketModelTestCases
):

    pass
