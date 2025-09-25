import inspect
import pytest

# from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import (
    ValidationError
)
from django.db import models

# from core.models.audit import CenturionAudit

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)


@pytest.mark.audit_models
class CenturionAuditModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):
        
        return {
            '_audit_enabled': {
                'value': False,
            },
            '_notes_enabled': {
                'value': False,
            },
            '_ticket_linkable': {
                'value': False,
            },
            'model_tag': {
                'type': type(None),
                'value': None,
            },
            'url_model_name': {
                'type': str,
                'value': 'centurionaudit',
            }
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'content_type': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'before': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.JSONField,
            'null': True,
            'unique': False,
        },
        'after': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.JSONField,
            'null': True,
            'unique': False,
        },
        'action': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
            'null': True,
            'unique': False,
        },
        'user': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'model_notes': {
            'blank': models.fields.NOT_PROVIDED,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.fields.NOT_PROVIDED,
            'null': models.fields.NOT_PROVIDED,
            'unique': models.fields.NOT_PROVIDED,}
    }


    @pytest.fixture( scope = 'class', autouse = True )
    def setup_vars(self, django_db_blocker, user, model):

        with django_db_blocker.unblock():

            try:

                content_type = ContentType.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )

            except ContentType.DoesNotExist:
                # Enable Abstract models to be tested

                content_type = ContentType.objects.get(
                    pk = 1,
                )



        self.kwargs_create_item.update({
            'content_type': content_type,
            'user': user,
        })


    @pytest.mark.xfail( reason = 'Does not require method' )
    def test_method_value_not_default___str__(self, model, model_instance ):
        """Test Method

        Ensure method `__str__` does not return the default value.
        """

        if model._meta.abstract:

            pytest.xfail(reason = 'Model is an abstract model')


        default_value = f'{model_instance._meta.object_name} object ({str(model_instance.id)})'

        assert model_instance.__str__() != default_value




class CenturionAuditModelInheritedCases(
    CenturionAuditModelTestCases,
):

    pass



class CenturionAuditModelPyTest(
    CenturionAuditModelTestCases,
):



    @pytest.mark.xfail( reason = 'This model is an abstract model')
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None


    def test_method_clean_fields_default_attributes(self, model_instance):
        """Test Class Method
        
        Ensure method `clean_fields`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.clean_fields)

        exclude = sig.parameters['exclude'].default

        assert(
            exclude == None
        )



    def test_method_get_model_history_default_attributes(self, model_instance):
        """Test Class Method
        
        Ensure method `get_model_history`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.get_model_history)

        model = sig.parameters['model'].default

        assert(
            model == inspect._empty
        )



    def test_method_get_model_history_model_missing__before(self, model_instance):
        """Test Class Method
        
        Ensure method `get_model_history` raises an exception if the model does
        not have attribute `_before` populated
        """

        default = model_instance.before
        model_instance.before = None

        with pytest.raises(ValidationError) as e:

            model_instance.get_model_history( model = model_instance )

        model_instance.before = default

        assert e.value.code == 'model_missing_before_data'



    def test_method_get_model_history_model_missing__after(self, model_instance):
        """Test Class Method
        
        Ensure method `get_model_history` raises an exception if the model does
        not have attribute `_after` populated
        """

        default = model_instance.after
        model_instance.after = None

        with pytest.raises(ValidationError) as e:

            model_instance._before = {'key': 'value'}

            model_instance.get_model_history( model = model_instance )

        del model_instance._before

        model_instance.after = default

        assert e.value.code == 'model_missing_after_data'



    def test_method_get_model_history_model_no_change(self, model_instance):
        """Test Class Method
        
        Ensure method `get_model_history` raises an exception if the models
        `_after` and `_before` attributes are te same
        """

        default_a = model_instance.after
        model_instance.after = None

        default_b = model_instance.before
        model_instance.before = None


        with pytest.raises(ValidationError) as e:

            model_instance._after = {'key': 'value'}
            model_instance._before = {'key': 'value'}

            model_instance.get_model_history( model = model_instance )

        del model_instance._after
        del model_instance._before

        model_instance.after = default_a
        model_instance.before = default_b

        assert e.value.code == 'before_and_after_same'



    def test_method_get_model_history_populates_field_after(self, model_instance):
        """Test Class Method
        
        Ensure method `get_model_history` correctly populates field `after`.
        """

        test_value = {'key_1': 'value_1'}
        model_instance._after = {'key': 'value', **test_value}
        model_instance._before = {'key': 'value'}


        model_instance.after = None


        model_instance.get_model_history( model = model_instance )

        del model_instance._after
        del model_instance._before

        assert model_instance.after == test_value



    def test_method_get_model_history_populates_field_before(self, model_instance):
        """Test Class Method
        
        Ensure method `get_model_history` correctly populates field `after`.
        """

        test_value = { 'key': 'value' }
        model_instance._after = { **test_value, 'key_1': 'value_1' }
        model_instance._before = { **test_value }


        model_instance.before = None


        model_instance.get_model_history( model = model_instance )

        del model_instance._after
        del model_instance._before

        assert model_instance.before == test_value
