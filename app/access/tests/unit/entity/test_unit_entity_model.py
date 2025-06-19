import pytest

from django.db import models

from access.models.entity import Entity

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_entity
class EntityModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': False
            },
            'model_tag': {
                'type': str,
                'value': 'entity'
            },
            'url_model_name': {
                'type': str,
                'value': 'entity'
            }
        }


    @property
    def parameterized_fields(self):

        return {
        'entity_type': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': False,
            'unique': True,
        },
        'modified': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': False,
            'unique': False,
        },
    }


    def test_class_inherits_entity(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, Entity)


    def test_function_value_get_related_model(self, model, model_instance):
        """Function test

        Confirm function `get_related_model` is of the sub-model type
        """

        assert type(model_instance.get_related_model()) == model


    def test_attribute_type_kb_model_name(self, model):
        """Attribute Type

        kb_model_name is of type str
        """

        assert type(model.kb_model_name) is str


    def test_attribute_value_kb_model_name(self, model):
        """Attribute Type

        kb_model_name has been set, override this test case with the value
        of attribute `kb_model_name`
        """

        assert model.kb_model_name == 'entity'



class EntityModelInheritedCases(
    EntityModelTestCases,
):
    pass



@pytest.mark.module_access
class EntityModelPyTest(
    EntityModelTestCases,
):

    def test_function_value_get_related_model(self, model_instance):
        """Function test

        Confirm function `get_related_model` is None for base model
        """

        assert model_instance.get_related_model() is None
