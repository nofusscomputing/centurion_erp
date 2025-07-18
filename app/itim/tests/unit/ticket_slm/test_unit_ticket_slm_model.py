import pytest

from django.db import models

from core.tests.unit.ticket_base.test_unit_ticket_base_model import TicketBaseModelInheritedCases

from itim.models.slm_ticket_base import SLMTicket



@pytest.mark.model_slmticket
class SLMTicketModelTestCases(
    TicketBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_notes_enabled': {
                'value': False
            },
            '_is_submodel': {
                'value': True
            },
            'model_tag': {
                'type': str,
                'value': 'ticket'
            },
            'url_model_name': {
                'type': str,
                'value': 'ticketbase'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            "tto": {
                'blank': True,
                'default': 0,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
            "ttr": {
                'blank': True,
                'default': 0,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
        }



    def test_class_inherits_SLMTicket(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, SLMTicket)


    def test_function_get_related_field_name_value(self, model):
        """Function test

        This test case overwrites a test of the same name. This model should
        return an empty string as it's the base model.

        Ensure that function `get_related_field_name` returns a string that is
        model the attribute the model exists under.
        """

        assert model().get_related_field_name() == ''


    def test_function_get_related_model_type(self, model):
        """Function test

        This test case overwrites a test of the same name. This model should
        return `None` as it's the base model.

        Ensure that function `get_related_model` returns a value that
        is of type `QuerySet`.
        """

        assert type(model().get_related_model()) is type(None)


    def test_method_get_url_kwargs(self, model_instance):

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'ticket_type': model_instance._meta.sub_model_type,
            'pk': model_instance.id
        }



class SLMTicketModelInheritedCases(
    SLMTicketModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_itim
class SLMTicketModelPyTest(
    SLMTicketModelTestCases,
):

    sub_model_type = 'slm'
