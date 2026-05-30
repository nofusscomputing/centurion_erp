import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_model import (
    TicketBaseModelInheritedTestCases
)



@pytest.mark.model_changeticket
class ChangeTicketModelTestCases(
    TicketBaseModelInheritedTestCases
):

    @property
    def parameterized_model_fields(self):

        return {}



class ChangeTicketModelInheritedTestCases(
    ChangeTicketModelTestCases
):

    pass


@pytest.mark.module_itim
class ChangeTicketModelPyTest(
    ChangeTicketModelTestCases
):

    pass
