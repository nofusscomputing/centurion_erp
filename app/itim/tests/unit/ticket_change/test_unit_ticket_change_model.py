import pytest

from django.db import models

from core.tests.unit.ticket_base.test_unit_ticket_base_model import TicketBaseModelInheritedCases

from itim.models.ticket_change import ChangeTicket



@pytest.mark.model_changeticket
class ChangeTicketModelTestCases(
    TicketBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {}


    @property
    def parameterized_model_fields(self):

        return {}



    def test_class_inherits_ChangeTicket(self, model):
        """ Class inheritence

        Model Must Inherit from changeticket
        """

        assert issubclass(model, ChangeTicket)


    def test_function_get_ticket_type(self, model):
        """Function test

        As this model is intended to be used alone.

        Ensure that function `get_ticket_type` returns `request` for model
        `RequestTicket`
        """

        assert model().get_ticket_type == 'change'



class ChangeTicketModelInheritedCases(
    ChangeTicketModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_itim
class ChangeTicketModelPyTest(
    ChangeTicketModelTestCases,
):

    sub_model_type = 'change'
