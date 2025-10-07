import importlib
import pytest

from django.apps import apps
from django.conf import settings
from django.db import models

# from core.models.centurion_notes import CenturionModelNote
from core.models.model_tickets import ModelTicket
from core.tests.unit.model_tickets_meta.test_unit_model_tickets_viewset_meta import (
    ModelTicketViewsetMetaInheritedCases
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

        if not issubclass(model, ModelTicket):
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



class ModelTicketMetaModelsViewSetTestCases(
    ModelTicketViewsetMetaInheritedCases
):
    """Model Ticket Meta Model Test Cases

    This test suite is the base for the dynamic tests that are created
    during pytest discover.
    """


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': self.model_class
            },
        }


    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker,
        clean_model_from_db, model,
        request, kwargs_modelticketmetamodel, model_contenttype,
    ):

        ticket_model = request.getfixturevalue(
            'model_' + request.cls.ticket_model_class._meta.model_name
        )

        def factory(
            ticket_model = ticket_model,
        ):

            ticket_model_kwargs = request.getfixturevalue(
                'kwargs_' + ticket_model._meta.model_name
            )()

            model_kwargs = kwargs_modelticketmetamodel()

            with django_db_blocker.unblock():

                kwargs_many_to_many = {}

                kwargs = {}

                for key, value in ticket_model_kwargs.items():

                    field = ticket_model._meta.get_field(key)

                    if isinstance(field, models.ManyToManyField):

                        kwargs_many_to_many.update({
                            key: value
                        })

                    else:

                        kwargs.update({
                            key: value
                        })


                model = ticket_model.objects.create( **kwargs )

                for key, value in kwargs_many_to_many.items():

                    field = getattr(model, key)

                    for entry in value:

                        field.add(entry)

            #     kwargs = {}


            model_kwargs.update({
                'model': model
            })

            request.cls.kwargs_create_item = model_kwargs

            return model_kwargs

        yield factory

        clean_model_from_db(ticket_model)
        clean_model_from_db(model)


    @pytest.fixture( scope = 'class' )
    def model(self, request, clean_model_from_db):

        yield request.cls.model_class

        clean_model_from_db(request.cls.model_class)


    @pytest.mark.skip( reason = 'ToDo: Figure out how to dynomagic add note_model instance' )
    def test_model_creation(self, model, user):
        pass

    @pytest.fixture( scope = 'class')
    def model_serializer(self, request):

        model = request.cls.ticket_model_class

        serializer_module = importlib.import_module(
            model._meta.app_label + '.serializers.' + str(
                request.cls.base_model._meta.model_name
                + '_' +
                model._meta.model_name
            )
        )

        yield {
            'base': getattr(serializer_module, 'BaseSerializer'),
            'model':  getattr(serializer_module, 'ModelSerializer'),
            'view':  getattr(serializer_module, 'ViewSerializer')
        }




for model in get_models():

    if(
        not issubclass(model, ModelTicket)
        or model == ModelTicket
    ):
        continue


    cls_name: str = f"{model._meta.object_name}MetaModelViewSetPyTest"

    dynamic_class = type(
        cls_name,
        (ModelTicketMetaModelsViewSetTestCases,),
        {
            'ticket_model_class': apps.get_model(
                app_label = model._meta.app_label,
                model_name = str( model._meta.object_name )[0:len(model._meta.object_name)-6]
            ),
            'model_class': model
        }
    )

    dynamic_class = pytest.mark.__getattr__(
        'model_' + str(model._meta.model_name)[0:len(model._meta.model_name)-6])(dynamic_class)
    dynamic_class = pytest.mark.__getattr__('module_' + model._meta.app_label)(dynamic_class)

    globals()[cls_name] = dynamic_class
