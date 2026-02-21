import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_viewset import (
    TicketBaseViewsetInheritedCases
)
from core.viewsets.ticket import (
    ViewSet,
)

from project_management.models.ticket_project_task import (
    ProjectTaskTicket
)



@pytest.mark.model_projecttaskticket
class ViewsetTestCases(
    TicketBaseViewsetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': ProjectTaskTicket
            },
        }



class ProjectTaskTicketViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTaskTicketViewsetPyTest(
    ViewsetTestCases,
):

    pass
