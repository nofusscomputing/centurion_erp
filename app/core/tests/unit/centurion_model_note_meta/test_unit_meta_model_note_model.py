import importlib

import pytest

from django.apps import apps
from django.conf import settings
from django.db import models

from centurion.tests.helpers import get_models

from core.models.audit import CenturionAudit
from core.models.centurion_notes import CenturionModelNote
from core.models.model_tickets import ModelTicket
from core.tests.unit.centurion_model_note_meta.test_unit_centurion_model_note_meta_model import (
    MetaAbstractModelInheritedCases
)



class ModelNotesMetaModelTestCases(
    MetaAbstractModelInheritedCases
):
    """AuditHistory Meta Model Test Cases

    This test suite is the base for the dynamic tests that are created
    during pytest discover.
    """

    @pytest.fixture( scope = 'class', autouse = True)
    def setup_organization(cls, request, organization_one):

        request.cls.organization = organization_one


    @pytest.fixture( scope = 'class' )
    def note_model(self, request):

        return request.cls.note_model_class


    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker,
        request, note_model, kwargs_centurionmodelnotemeta
    ):

        request.cls.kwargs_create_item = {}

        model_objs = []
        def factory(model_objs = model_objs):

            model_kwargs = kwargs_centurionmodelnotemeta()

            with django_db_blocker.unblock():

                note_model_kwargs = request.getfixturevalue('kwargs_' + note_model._meta.model_name)()

                kwargs = {}

                many_field = {}

                for field, value in note_model_kwargs.items():

                    if not hasattr(getattr(note_model, field), 'field'):
                        continue

                    if isinstance(getattr(note_model, field).field, models.ManyToManyField):

                        if field in many_field:

                            many_field[field] += [ value ]

                        elif isinstance(value, list):

                            value_list = []

                            for list_value in value:

                                value_list += [ list_value ]


                            value = value_list

                        else:

                            many_field.update({
                                field: [
                                    value
                                ]
                            })

                        continue

                    kwargs.update({
                        field: value
                    })


                model = note_model.objects.create(
                    **kwargs
                )

                model_objs += [ model ]


                for field, values in many_field.items():

                    for value in values:

                        getattr(model, field).add( value )


            model_kwargs.update({
                'model': model
            })
            request.cls.kwargs_create_item.update( **model_kwargs )

            return model_kwargs

        yield factory

        with django_db_blocker.unblock():

            for obj in model_objs:
                obj.delete()


    @pytest.fixture( scope = 'class' )
    def model(self, request):

        return request.cls.model_class


    @pytest.fixture( scope = 'class')
    def model_serializer(self, model):

        serializer_name: str =  'centurionmodelnote_' + str(model._meta.model_name).replace('centurionmodelnote', '')

        serializer_module = importlib.import_module(
                    name = model._meta.app_label + '.serializers.' + str(
                        serializer_name
                    )
                )


        yield {
            'view': getattr( serializer_module, 'ViewSerializer' )
        }



    @pytest.mark.skip( reason = 'ToDo: Figure out how to dynomagic add note_model instance' )
    def test_model_creation(self, model, user):
        pass



for model in get_models(
    excludes = [
        'manufacturer'
    ],
    excludes_model_classes = [
            CenturionAudit,
            CenturionModelNote,
            ModelTicket
    ],
):


    cls_name: str = f"{model._meta.object_name}MetaModelPyTest"

    dynamic_class = type(
        cls_name,
        (ModelNotesMetaModelTestCases,),
        {
            'note_model_class': apps.get_model(
                app_label = model._meta.app_label,
                model_name = str( model._meta.object_name ).replace('CenturionModelNote', '')
            ),
            'model_class': model
        }
    )

    dynamic_class = pytest.mark.__getattr__(
        'model_' + str(model._meta.model_name).replace('centurionmodelnote', ''))(dynamic_class)
    dynamic_class = pytest.mark.__getattr__('module_' + model._meta.app_label)(dynamic_class)

    globals()[cls_name] = dynamic_class
