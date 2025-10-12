import pytest

from django.db import models

from access.models.entity import Entity

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_entity
class EntityModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_base_model': {
                'type': models.base.ModelBase,
                'value': Entity,
            },
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


    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'model_name': model_instance._meta.model_name,
            'pk': model_instance.id
        }




class EntityModelInheritedCases(
    EntityModelTestCases,
):
    pass



@pytest.mark.module_access
class EntityModelPyTest(
    EntityModelTestCases,
):

    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'pk': model_instance.id
        }
