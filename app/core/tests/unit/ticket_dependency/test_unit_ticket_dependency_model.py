import pytest

from django.db import models

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.tickets
@pytest.mark.model_ticketdependency
class TicketDependencyModelTestCases(
    CenturionAbstractTenancyModelInheritedCases,
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_base_model': {
                'type': type(None),
                'value': None,
            },
            '_audit_enabled': {
                'value': False
            },
            '_is_submodel': {
                'value': False
            },
            '_notes_enabled': {
                'value': False
            },
            '_ticket_linkable': {
                'value': False,
            },
            'model_tag': {
                'type': type(None),
                'value': None,
            },
            'page_layout': {
                'type': type(None),
                'value': None,
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            "model_notes": {
                'blank': models.fields.NOT_PROVIDED,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.NOT_PROVIDED,
                'null': models.fields.NOT_PROVIDED,
                'unique': models.fields.NOT_PROVIDED,
            },
            "ticket": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            "how_related": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.IntegerField,
                'null': False,
                'unique': False,
            },
            "dependent_ticket": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
        }



    def test_method_get_url_kwargs(self, mocker, model_instance, settings):

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'ticket_id': model_instance.ticket.id,
            'pk': model_instance.id,
        }


    def test_model_tag_defined(self, model):
        pytest.xfail( reason = 'Model does not use model tag. test is N/A.' )


    def test_model_tag_not_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is None



class TicketDependencyModelInheritedCases(
    TicketDependencyModelTestCases,
):
    pass


@pytest.mark.module_core
class TicketDependencyModelPyTest(
    TicketDependencyModelTestCases,
):

    pass
