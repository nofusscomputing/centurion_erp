import pytest

from itim.tests.functional.ticket_slm.test_functional_ticket_slm_model import (
    SLMTicketModelInheritedTestCases
)


@pytest.mark.model_incidentticket
class IncidentTicketModelTestCases(
    SLMTicketModelInheritedTestCases
):
    pass


class IncidentTicketModelInheritedTestCases(
    IncidentTicketModelTestCases
):

    pass


@pytest.mark.module_itim
class IncidentTicketModelPyTest(
    IncidentTicketModelTestCases
):

    pass
