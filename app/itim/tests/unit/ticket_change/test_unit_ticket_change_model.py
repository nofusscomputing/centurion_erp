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



class ChangeTicketModelInheritedCases(
    ChangeTicketModelTestCases,
):
    pass



@pytest.mark.module_itim
class ChangeTicketModelPyTest(
    ChangeTicketModelTestCases,
):
    pass
