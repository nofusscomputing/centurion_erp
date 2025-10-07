import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_operatingsystemversion
class OperatingSystemVersionModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'value': 'operating_system_version'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'operating_system': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            'name': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 50,
                'null': False,
                'unique': False,
            },
            'modified': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            }
        }



class OperatingSystemVersionModelInheritedCases(
    OperatingSystemVersionModelTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemVersionModelPyTest(
    OperatingSystemVersionModelTestCases,
):
    pass

    def test_method_get_url_kwargs(self, mocker, model_instance, model_kwargs):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'operating_system_id': model_instance.operating_system.id,
            'pk': model_instance.id
        }


    # def test_model_tag_defined(self, model):
    #     """ Model Tag

    #     Ensure that the model has a tag defined.
    #     """

    #     pytest.xfail( reason = 'model does not require' )


    # def test_method_value_not_default___str__(self, model, model_instance ):
    #     """Test Method

    #     Ensure method `__str__` does not return the default value.
    #     """

    #     pytest.xfail( reason = 'model does not require' )
