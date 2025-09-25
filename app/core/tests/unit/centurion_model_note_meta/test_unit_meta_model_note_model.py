import pytest

from django.apps import apps
from django.conf import settings
from django.db import models

from core.models.centurion_notes import CenturionModelNote
from core.tests.unit.centurion_model_note_meta.test_unit_centurion_model_note_meta_model import (
    MetaAbstractModelInheritedCases
)



def get_models( excludes: list[ str ] = [] ) -> list[ tuple ]:
    """Fetch models from Centurion Apps

    Args:
        excludes (list[ str ]): Words that may be in a models name to exclude

    Returns:
        list[ tuple ]: Centurion ERP Only models
    """

    models: list = []

    model_apps: list = []

    exclude_model_apps = [
        'django',
        'django_celery_results',
        'django_filters',
        'drf_spectacular',
        'drf_spectacular_sidecar',
        'coresheaders',
        'corsheaders',
        'rest_framework',
        'rest_framework_json_api',
        'social_django',
    ]

    for app in settings.INSTALLED_APPS:

        app = app.split('.')[0]

        if app in exclude_model_apps:
            continue

        model_apps += [ app ]


    for model in apps.get_models():

        model_name = str(model._meta.model_name)

        if(
            model._meta.app_label not in model_apps
            or model_name.endswith('ticket') and len(model_name) > 6
        ):
            continue

        skip = False

        for exclude in excludes:

            if exclude in str(model._meta.model_name):
                skip = True
                break

        if skip:
                continue

        models += [ model ]

    return models



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

        model_kwargs = kwargs_centurionmodelnotemeta.copy()

        with django_db_blocker.unblock():

            note_model_kwargs = request.getfixturevalue('kwargs_' + note_model._meta.model_name)
            if callable(note_model_kwargs):
                note_model_kwargs = note_model_kwargs()

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


            for field, values in many_field.items():

                for value in values:

                    getattr(model, field).add( value )


        model_kwargs.update({
            'model': model
        })
        request.cls.kwargs_create_item = model_kwargs

        yield model_kwargs

        with django_db_blocker.unblock():

            model.delete()


    @pytest.fixture( scope = 'class' )
    def model(self, request):

        return request.cls.model_class


    @pytest.mark.skip( reason = 'ToDo: Figure out how to dynomagic add note_model instance' )
    def test_model_creation(self, model, user):
        pass



for model in get_models():

    if(
        not issubclass(model, CenturionModelNote)
        or model == CenturionModelNote
    ):
        continue


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
