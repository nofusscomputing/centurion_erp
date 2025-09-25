import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_deviceoperatingsystem
class DeviceOperatingSystemModelTestCases(
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
            '_ticket_linkable': {
                'value': False,
            },
            'model_tag': {
                'type': models.fields.NOT_PROVIDED,
                'value': models.fields.NOT_PROVIDED
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
            'device': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': True,
            },
            'operating_system_version': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            'version': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 15,
                'null': False,
                'unique': False,
            },
            'installdate': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': True,
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



class DeviceOperatingSystemModelInheritedCases(
    DeviceOperatingSystemModelTestCases,
):
    pass


@pytest.mark.module_itam
class DeviceOperatingSystemModelPyTest(
    DeviceOperatingSystemModelTestCases,
):

    def test_method_get_url_kwargs(self, mocker, model_instance, model_kwargs):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'device_id': model_kwargs['device'].id,
            'pk': model_instance.id
        }


    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        pytest.xfail( reason = 'model does not require' )


    def test_method_value_not_default___str__(self, model, model_instance ):
        """Test Method

        Ensure method `__str__` does not return the default value.
        """

        pytest.xfail( reason = 'model does not require' )
