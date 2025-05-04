from django.db import models

from core.tests.unit.ticket_base.test_unit_ticket_base_model import TicketBaseModelInheritedCases

from itim.models.slm_ticket_base import SLMTicket



class SLMTicketModelTestCases(
    TicketBaseModelInheritedCases,
):

    kwargs_create_item: dict = {
        'tto': 1,
        'ttr': 2,
    }

    parameterized_fields: dict = {
        "tto": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': 0,
            'field_parameter_verbose_name_type': str
        },
        "ttr": {
            'field_type': models.fields.IntegerField,
            'field_parameter_default_exists': True,
            'field_parameter_default_value': 0,
            'field_parameter_verbose_name_type': str
        },
    }

    sub_model_type = 'slm'


    def test_class_inherits_slmticket(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, SLMTicket)


    def test_function_get_ticket_type(self):
        """Function test

        As this model is not intended to be used alone.

        Ensure that function `get_ticket_type` returns None for model
        `SLMTicket`
        """

        assert self.model().get_ticket_type == None



class SLMTicketModelInheritedCases(
    SLMTicketModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model SLMTicket
    """

    kwargs_create_item: dict = None

    model = None

    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """



class SLMTicketModelPyTest(
    SLMTicketModelTestCases,
):

    pass
