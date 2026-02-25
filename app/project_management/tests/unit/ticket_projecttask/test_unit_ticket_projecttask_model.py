import pytest

from django.db import models

from core.tests.unit.ticket_base.test_unit_ticket_base_model import TicketBaseModelInheritedCases

from project_management.models.ticket_project_task import ProjectTaskTicket



@pytest.mark.model_projecttaskticket
class ProjectTaskTicketModelTestCases(
    TicketBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {}


    @property
    def parameterized_model_fields(self):

        return {}



    def test_class_inherits_ProjectTaskTicket(self, model):
        """ Class inheritence

        Model Must Inherit from projecttaskticket
        """

        assert issubclass(model, ProjectTaskTicket)



class ProjectTaskTicketModelInheritedCases(
    ProjectTaskTicketModelTestCases,
):
    pass



@pytest.mark.module_project_management
class ProjectTaskTicketModelPyTest(
    ProjectTaskTicketModelTestCases,
):
    pass
