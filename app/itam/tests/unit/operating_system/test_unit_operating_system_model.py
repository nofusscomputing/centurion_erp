import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_operatingsystem
class OperatingSystemModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'value': 'operating_system'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'publisher': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            'name': {
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



class OperatingSystemModelInheritedCases(
    OperatingSystemModelTestCases,
):
    pass



@pytest.mark.module_itam
class OperatingSystemModelPyTest(
    OperatingSystemModelTestCases,
):
    pass

    # def test_method_get_url_kwargs(self, mocker, model_instance, model_kwargs):
    #     """Test Class Method
        
    #     Ensure method `get_url_kwargs` returns the correct value.
    #     """


    #     url = model_instance.get_url_kwargs()

    #     assert model_instance.get_url_kwargs() == {
    #         'device_id': model_kwargs['device'].id,
    #         'pk': model_instance.id
    #     }


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
