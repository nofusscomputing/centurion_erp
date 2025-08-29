import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_appsettings
class AppSettingsModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_notes_enabled': {
                'value': False
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
            'organization': {
                'blank': models.fields.NOT_PROVIDED,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.NOT_PROVIDED,
                'null': models.fields.NOT_PROVIDED,
                'unique': models.fields.NOT_PROVIDED,
            },
            'owner_organization': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            'device_model_is_global': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'device_type_is_global': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'manufacturer_is_global': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'software_is_global': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'software_categories_is_global': {
                'blank': False,
                'default': False,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            'owner_organization': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
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



class AppSettingsModelInheritedCases(
    AppSettingsModelTestCases,
):
    pass



@pytest.mark.module_settings
class AppSettingsModelPyTest(
    AppSettingsModelTestCases,
):

    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        pytest.xfail( reason = 'Model does not require tag' )


    def test_method_value_not_default___str__(self, model, model_instance ):
        """Test Method

        Ensure method `__str__` does not return the default value.
        """

        pytest.xfail( reason = 'Model does not require this function' )


    def test_method_get_tenant_returns_tenant(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `get_history_model_name` returns the value of the models
        audit name `<Model Class name>AuditHistory`
        """

        test_value = self.organization
        model_instance.owner_organization = test_value


        assert model_instance.get_tenant() == test_value
