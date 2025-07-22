import pytest

from django.db import models

from django.utils.timezone import now

from api.models.tokens import AuthToken

from core.tests.unit.mixin_centurion.test_unit_centurion_mixin import CenturionMixnInheritedCases



@pytest.mark.unit
@pytest.mark.centurion_models
class AuthTokenModelTestCases(
    CenturionMixnInheritedCases,
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'type': bool,
                'value': False,
            },
            '_is_submodel': {
                'type': bool,
                'value': False,
            },
            '_notes_enabled': {
                'type': bool,
                'value': False,
            },
            'model_tag': {
                'type': models.fields.NOT_PROVIDED,
                'value': models.fields.NOT_PROVIDED,
            },
            'url_model_name': {
                'type': type(None),
                'value': None,
            }
        }

    @property
    def parameterized_model_fields(self):

        return {
            'id': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.IntegerField,
                'null': False,
                'unique': True,
            },
            'note': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 50,
                'null': True,
                'unique': False,
            },
            'token': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'length': 64,
                'null': False,
                'unique': True,
            },
            'user': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
            'expires': {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            },
            'created': {
                'blank': False,
                'default': now,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            },
            'modified': {
                'blank': False,
                'default': now,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            },
        }



    def test_class_inherits_centurion_model(self, model):
        """ Class Check

        Ensure this model inherits from `AuthToken`
        """

        assert issubclass(model, AuthToken)



    def test_method_get_url_kwargs(self, mocker, model_instance, settings):
        """Test Class Method
        
        Ensure method `get_url_kwargs` returns the correct value.
        """


        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == { 'model_id': model_instance.user.id, 'pk': model_instance.id }



    def test_model_tag_defined(self, model):
        pytest.mark.xfail( reason = 'model does not use tag' )




class AuthTokenModelInheritedCases(
    AuthTokenModelTestCases,
):

    pass



class AuthTokenModelPyTest(
    AuthTokenModelTestCases,
):
    pass
