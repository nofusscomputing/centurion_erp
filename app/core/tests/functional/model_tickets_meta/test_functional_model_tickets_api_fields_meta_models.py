import importlib
import pytest

from django.apps import apps
from django.conf import settings
from django.db import models

# from core.models.centurion_notes import CenturionModelNote
from core.models.model_tickets import ModelTicket

from core.tests.functional.model_tickets_meta.test_functional_model_tickets_api_fields_meta import (
    ModelTicketMetaAPIInheritedCases
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



class ModelTicketMetaModelsAPITestCases(
    ModelTicketMetaAPIInheritedCases
):
    """Model Ticket Meta Model Test Cases

    This test suite is the base for the dynamic tests that are created
    during pytest discover.
    """


    @property
    def parameterized_api_fields(self):

        return {
            # 'model': {
            #     # 'expected': models.NOT_PROVIDED,
            #     'type': int,
            # },
            # 'model_notes': {
            #     'expected': models.NOT_PROVIDED,
            #     'type': models.NOT_PROVIDED,
            # },
            # 'content_type': {
            #     'expected': dict
            # },
            # 'content_type.id': {
            #     'expected': int
            # },
            # 'content_type.display_name': {
            #     'expected': str
            # },
            # 'content_type.url': {
            #     'expected': Hyperlink
            # },
            # 'ticket': {
            #     'expected': dict
            # },
            # 'ticket.id': {
            #     'expected': int
            # },
            # 'ticket.display_name': {
            #     'expected': str
            # },
            # 'ticket.url': {
            #     'expected': str
            # },
            # 'modified': {
            #     'expected': str
            # }
        }



    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker,
        request, kwargs_modelticketmetamodel, model_contenttype,
    ):

        model_kwargs = kwargs_modelticketmetamodel()

        with django_db_blocker.unblock():

            ticket_model = request.getfixturevalue(
                'model_' + request.cls.ticket_model_class._meta.model_name
            )

            ticket_model_kwargs = request.getfixturevalue(
                'kwargs_' + ticket_model._meta.model_name
            )()


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

        yield model_kwargs

        with django_db_blocker.unblock():

            model.delete()


    @pytest.fixture( scope = 'class' )
    def model(self, request):

        return request.cls.model_class


    @pytest.fixture( scope = 'class')
    def create_model(self, request, django_db_blocker,
        model, model_kwargs, organization_one
    ):


        item = None

        with django_db_blocker.unblock():

            kwargs_many_to_many = {}

            kwargs = {}

            for key, value in model_kwargs.items():

                field = model._meta.get_field(key)

                if isinstance(field, models.ManyToManyField):

                    kwargs_many_to_many.update({
                        key: value
                    })

                else:

                    kwargs.update({
                        key: value
                    })

            if request.cls.ticket_model_class._meta.model_name == 'tenant':
                kwargs['organization'] = organization_one
                kwargs['model'] = organization_one

            item = model.objects.create(
                **kwargs
            )

            for key, value in kwargs_many_to_many.items():

                field = getattr(item, key)

                for entry in value:

                    field.add(entry)

            request.cls.item = item

        yield item

        with django_db_blocker.unblock():

            item.delete()


    # @pytest.fixture( scope = 'class')
    # def model_serializer(self, request):

    #     model = request.cls.ticket_model_class

    #     serializer_module = importlib.import_module(
    #         model._meta.app_label + '.serializers.' + str(
    #             request.cls.base_model._meta.model_name
    #             + '_' +
    #             model._meta.model_name
    #         )
    #     )

    #     yield {
    #         'base': getattr(serializer_module, 'BaseSerializer'),
    #         'model':  getattr(serializer_module, 'ModelSerializer'),
    #         'view':  getattr(serializer_module, 'ViewSerializer')
    #     }




for model in get_models():

    if(
        not issubclass(model, ModelTicket)
        or model == ModelTicket
    ):
        continue


    cls_name: str = f"{model._meta.object_name}MetaModelAPIPermissionPyTest"

    dynamic_class = type(
        cls_name,
        (ModelTicketMetaModelsAPITestCases,),
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
