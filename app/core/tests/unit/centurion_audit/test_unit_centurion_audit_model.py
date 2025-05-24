import inspect
import pytest

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models.audit import CenturionAudit

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)


@pytest.mark.models
class CenturionAuditModelTestCases(
    CenturionAbstractModelInheritedCases
):


    kwargs_create_item = {
            'before': {},
            'after': {
                'after_key': 'after_value'
            },
            'action': CenturionAudit.Actions.ADD,
            'user': 'fixture sets value',
            'content_type': 'fixture sets value',
        }


    parameterized_class_attributes = {
        '_audit_enabled': {
            'value': False,
        },
        '_notes_enabled': {
            'value': False,
        }
    }


    parameterized_model_fields = {
        'content_type': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.IntegerField,
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
        }
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


class CenturionAuditModelInheritedCases(
    CenturionAuditModelTestCases,
):

    pass



class CenturionAuditModelPyTest(
    CenturionAuditModelTestCases,
):


    def test_method_clean_fields_default_attributes(self, model_instance):
        """Test Class Method
        
        Ensure method `clean_fields`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.clean_fields)

        exclude = sig.parameters['exclude'].default

        assert(
            exclude == None
        )



    def test_method_clean_fields_calls_super_clean_fields(self, mocker, model_instance):
        """Test Class Method
        
        Ensure method `clean_fields` calls `super().clean_fields` with the defined attributes.
        """

        super_clean_fields = mocker.patch('core.models.centurion.CenturionModel.clean_fields', return_value = None)

        model_instance.clean_fields()


        super_clean_fields.assert_called_with(
            exclude = None
        )



    def test_method_clean_fields_not_implemented_exception(self, mocker, model):
        """Test Class Method
        
        Ensure method `clean_fields` raises an exception if the child model
        does not implement its own method of the same name.
        """

        class MockModel(model):
            class Meta:
                app_label = 'core'
                verbose_name = 'mock instance'
                managed = False

        mock_model = MockModel()

        del apps.all_models['core']['mockmodel']

        super_clean_fields = mocker.patch('core.models.centurion.CenturionModel.full_clean', return_value = None)

        with pytest.raises(NotImplementedError):

            mock_model.clean_fields()



    def test_method_get_model_history_default_attributes(self, model_instance):
        """Test Class Method
        
        Ensure method `get_model_history`  has the defined default attributes.
        """

        sig = inspect.signature(model_instance.get_model_history)

        model = sig.parameters['model'].default

        assert(
            model == inspect._empty
        )
