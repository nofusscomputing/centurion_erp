import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_model import (
    TicketBaseModelInheritedTestCases
)



@pytest.mark.model_projecttaskticket
class ProjectTaskTicketModelTestCases(
    TicketBaseModelInheritedTestCases
):

    @property
    def parameterized_model_fields(self):

        return {}



class ProjectTaskTicketModelInheritedTestCases(
    ProjectTaskTicketModelTestCases
):

    pass


@pytest.mark.module_project_management
class ProjectTaskTicketModelPyTest(
    ProjectTaskTicketModelTestCases
):

    pass
