
import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)



@pytest.mark.model_projecttaskticket
class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):
    pass



class ProjectTaskTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTaskTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
