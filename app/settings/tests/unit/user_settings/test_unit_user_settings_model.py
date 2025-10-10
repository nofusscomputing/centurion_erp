import pytest

from django.db import models
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from access.tests.unit.managers.test_unit_user_manager import (
    UserManagerInheritedCases
)

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)

from settings.models.user_settings import UserSettings



@pytest.mark.model_usersettings
class UserSettingsModelTestCases(
    UserManagerInheritedCases,
    CenturionAbstractTenancyModelInheritedCases,
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
            'organization': {
                'blank': models.fields.NOT_PROVIDED,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.fields.NOT_PROVIDED,
                'null': models.fields.NOT_PROVIDED,
                'unique': models.fields.NOT_PROVIDED,
            },
            'user': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            'browser_mode': {
                'blank': False,
                'default': UserSettings.BrowserMode.AUTO,
                'field_type': models.IntegerField,
                'null': False,
                'unique': False,
            },
            'default_organization': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': True,
                'unique': False,
            },
            'timezone': {
                'blank': False,
                'default': 'UTC',
                'field_type': models.CharField,
                'length': 32,
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


    def test_add_create_not_allowed(self, model):
        """ Check correct permission for add 

        Not allowed to add.
        Ensure that the list view for HTTP/POST does not exist.
        """

        with pytest.raises( NoReverseMatch ) as e:

            reverse('v2:' + model._meta.model_name + '-list')

    def test_manager_tenancy_filter_tenant(self):
        pytest.xfail( reason = 'base model, test is n/a.' )

    def test_manager_tenancy_select_related(self):
        pytest.xfail( reason = 'base model, test is n/a.' )


    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == { 'user_id': model_instance.user.id }



class UserSettingsModelInheritedCases(
    UserSettingsModelTestCases,
):
    pass



@pytest.mark.module_settings
class UserSettingsModelPyTest(
    UserSettingsModelTestCases,
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
