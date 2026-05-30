import pytest

from core.tests.functional.ticket_base.test_functional_ticket_base_api_fields import (
    TicketBaseAPIInheritedCases,
)



@pytest.mark.model_projecttaskticket
class ProjectTaskTicketAPITestCases(
    TicketBaseAPIInheritedCases,
):

    @property
    def parameterized_api_fields(self):

        return {}



class ProjectTaskTicketAPIInheritedCases(
    ProjectTaskTicketAPITestCases,
):

    pass



@pytest.mark.module_project_management
class ProjectTaskTicketAPIPyTest(
    ProjectTaskTicketAPITestCases,
):

    pass
