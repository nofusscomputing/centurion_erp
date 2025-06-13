import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_softwareenablefeatureflag
class SoftwareEnableFeatureFlagModelTestCases(
    CenturionAbstractModelInheritedCases
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
            'model_tag': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED
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
        'software': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'enabled': {
            'blank': False,
            'default': False,
            'field_type': models.IntegerField,
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



class SoftwareEnableFeatureFlagModelInheritedCases(
    SoftwareEnableFeatureFlagModelTestCases,
):
    pass



@pytest.mark.module_devops
class SoftwareEnableFeatureFlagModelPyTest(
    SoftwareEnableFeatureFlagModelTestCases,
):

    def test_method_get_url_kwargs(self, mocker, model_instance, model_kwargs):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'software_id': model_kwargs['software'].id,
            'pk': model_instance.id
        }


    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        pytest.xfail( reason = 'model does not require' )
