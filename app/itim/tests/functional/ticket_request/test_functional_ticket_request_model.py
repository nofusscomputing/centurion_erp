import pytest

from itim.tests.functional.ticket_slm.test_functional_ticket_slm_model import (
    SLMTicketModelInheritedTestCases
)


@pytest.mark.model_requestticket
class RequestTicketModelTestCases(
    SLMTicketModelInheritedTestCases
):
    pass


class RequestTicketModelInheritedTestCases(
    RequestTicketModelTestCases
):

    pass


@pytest.mark.module_itim
class RequestTicketModelPyTest(
    RequestTicketModelTestCases
):

    pass
