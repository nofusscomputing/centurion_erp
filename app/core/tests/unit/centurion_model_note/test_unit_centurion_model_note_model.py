import inspect
import pytest

from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)


@pytest.mark.note_models
class CenturionNoteModelTestCases(
    CenturionAbstractModelInheritedCases
):


    parameterized_class_attributes = {
        '_audit_enabled': {
            'value': False,
        },
        '_notes_enabled': {
            'value': False,
        },
        'model_tag': {
            'type': type(None),
            'value': None,
        },
        'url_model_name': {
            'type': str,
            'value': 'centurionmodelnote',
        }
    }


    parameterized_model_fields = {
        'body': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': False,
            'unique': False,
        },
        'created_by': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'modified_by': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'content_type': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
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
        'model_notes': {
            'blank': models.fields.NOT_PROVIDED,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.fields.NOT_PROVIDED,
            'null': models.fields.NOT_PROVIDED,
            'unique': models.fields.NOT_PROVIDED,
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
            'created_by': user,
        })



    @pytest.mark.xfail( reason = 'Model does not require method' )
    def test_method_value_not_default___str__(self, model, model_instance ):
        """Test Method

        Ensure method `__str__` does not return the default value.
        """

        if model._meta.abstract:

            pytest.xfail(reason = 'Model is an abstract model')


        default_value = f'{model_instance._meta.object_name} object ({str(model_instance.id)})'

        assert model_instance.__str__() != default_value




class CenturionNoteModelInheritedCases(
    CenturionNoteModelTestCases,
):

    pass



class CenturionNoteModelPyTest(
    CenturionNoteModelTestCases,
):



    @pytest.mark.xfail( reason = 'This model is an abstract model')
    def test_model_tag_defined(self, model):
        """ Model Tag

        Ensure that the model has a tag defined.
        """

        assert model.model_tag is not None
