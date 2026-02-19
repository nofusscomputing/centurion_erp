import pytest

from django.db import models

from core.tests.unit.ticket_base.test_unit_ticket_base_model import TicketBaseModelInheritedCases

from itim.models.ticket_problem import ProblemTicket



@pytest.mark.model_problemticket
class ProblemTicketModelTestCases(
    TicketBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {}


    @property
    def parameterized_model_fields(self):

        return {
            "business_impact": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.TextField,
                'null': True,
                'unique': False,
            },
            "cause_analysis": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.TextField,
                'null': True,
                'unique': False,
            },
            "observations": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.TextField,
                'null': True,
                'unique': False,
            },
            "workaround": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.TextField,
                'null': True,
                'unique': False,
            },
        }



    def test_class_inherits_ProblemTicket(self, model):
        """ Class inheritence

        Model Must Inherit from problemticket
        """

        assert issubclass(model, ProblemTicket)



    def test_function_get_ticket_type(self, model):

        assert model().get_ticket_type == 'problem'



class ProblemTicketModelInheritedCases(
    ProblemTicketModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_itim
class ProblemTicketModelPyTest(
    ProblemTicketModelTestCases,
):

    sub_model_type = 'problem'
