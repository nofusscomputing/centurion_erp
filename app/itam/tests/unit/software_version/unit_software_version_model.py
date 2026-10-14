import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_softwareversion
class SoftwareVersionModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'value': 'software_version'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            'software': {
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
            },
        }



class SoftwareVersionModelInheritedCases(
    SoftwareVersionModelTestCases,
):
    pass



@pytest.mark.module_itam
class SoftwareVersionModelPyTest(
    SoftwareVersionModelTestCases,
):

    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """

        assert model_instance.get_url_kwargs() == { 'pk': model_instance.id, 'software_id': model_instance.software.id }

