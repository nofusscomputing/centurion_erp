import pytest

from django.db import models

from core.models.model_tickets import ModelTicket, TicketBase
from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractBaseModelInheritedCases
)
from core.tests.unit.manager_ticketmodel.test_unit_ticket_model_manager import (
    TicketModelManagerInheritedCases
)




@pytest.mark.tickets
@pytest.mark.model_modelticket
class ModelTicketModelTestCases(
    TicketModelManagerInheritedCases,
    CenturionAbstractBaseModelInheritedCases,
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_base_model': {
                'type': models.base.ModelBase,
                'value': ModelTicket
            },
            '_notes_enabled': {
                'value': False
            },
            '_ticket_linkable': {
                'value': False
            },
            'model_notes': {
                'type': type(None),
                'value': None
            },
            'model_tag': {
                'type': type(None),
                'value': None
            },
            'url_model_name': {
                'type': str,
                'value': 'modelticket'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'model_notes': {
                'blank': models.fields.NOT_PROVIDED,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.NOT_PROVIDED,
                'null': models.fields.NOT_PROVIDED,
                'unique': models.fields.NOT_PROVIDED,
            },
            'content_type': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            'ticket': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            'modified': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            },
        }


    def test_model_tag_defined(self, model):
        pytest.xfail( reason = 'model is for linking to ticket, test is N/A.')


    def test_method_get_url_kwargs(self, mocker, model, model_instance, settings):

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is an abstract model. test not required.' )

        assert model_instance.get_url_kwargs() == {
            'model_name': model_instance.ticket._meta.model_name,
            'model_id': model_instance.ticket.pk,
            'pk': model_instance.id 
        }



class ModelTicketModelInheritedCases(
    ModelTicketModelTestCases,
):
    pass



@pytest.mark.module_core
class ModelTicketModelPyTest(
    ModelTicketModelTestCases,
):

    def test_manager_ticketmodel_filter_tenant(self):
        pytest.xfail( reason = 'filtering requires field model which is not avail in base model.' )


    def test_manager_ticketmodel_select_related(self):
        pytest.xfail( reason = 'filtering requires field model which is not avail in base model.' )
