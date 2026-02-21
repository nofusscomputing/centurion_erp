import pytest

from core.tests.unit.ticket_base.test_unit_ticket_base_serializer import (
    TicketBaseSerializerInheritedCases
)



@pytest.mark.model_projecttaskticket
class ProjectTaskTicketSerializerTestCases(
    TicketBaseSerializerInheritedCases
):
    pass



class ProjectTaskTicketSerializerInheritedCases(
    ProjectTaskTicketSerializerTestCases
):
    pass



@pytest.mark.module_project_management
class ProjectTaskTicketSerializerPyTest(
    ProjectTaskTicketSerializerTestCases
):
    pass