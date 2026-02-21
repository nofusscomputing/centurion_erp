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


    def test_function_get_ticket_type(self, model):
        """Function test

        As this model is intended to be used alone.

        Ensure that function `get_ticket_type` returns `request` for model
        `RequestTicket`
        """

        assert model().get_ticket_type == 'projecttask'



class ProjectTaskTicketModelInheritedCases(
    ProjectTaskTicketModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_project_management
class ProjectTaskTicketModelPyTest(
    ProjectTaskTicketModelTestCases,
):

    sub_model_type = 'projecttask'
