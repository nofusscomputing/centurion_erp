import pytest

from django.apps import apps
from django.conf import settings
from django.core.exceptions import (
    ValidationError
)
from django.db import models

from core.models.model_tickets import ModelTicketMetaModel
from core.tests.functional.model_tickets.test_functional_model_tickets_model import (
    ModelTicketModelInheritedCases
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

        if not issubclass(model, ModelTicketMetaModel):
            continue

        if(
            model._meta.app_label not in model_apps
        ):
            continue

        skip = False

        for exclude in excludes:

            if exclude in model_name:
                skip = True
                break

        if skip:
                continue

        models += [ model ]

    return models


def make_fixture_with_args(arg_names, func, decorator_factory=None, decorator_args=None):
    args_str = ", ".join(arg_names)

    src = f"""
@decorator_factory(**decorator_args)
def _generated(self, {args_str}):
    yield from func(self, {args_str})
"""

    local_ns = {}
    global_ns = {
        "func": func,
        "decorator_factory": decorator_factory,
        "decorator_args": decorator_args,
    }

    exec(src, global_ns, local_ns)
    return local_ns["_generated"]




def model(self, model__model_name):

    yield self.test_model



exclude_model_from_test = [
    'ConfigGroupHosts',    # No API Endpoint
]


class ModelTicketMetaModelTestCases(
    ModelTicketModelInheritedCases
):
    """API Permission Test Cases

    This test suite is dynamically created for `Centurion` sub-classes.
    Each `Centurion` must ensure their model fixture exists in
    `tests/fixtures/model_<model_name>` with fixtures `model_<model_name>` and
    `kwargs_<model_name>` defined.
    """


    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker,
        request, kwargs_modelticketmetamodel, model_contenttype,
        model, organization_one
    ):

        model_objs = []
        def factory( model_objs = model_objs, model = model):

            model_kwargs = kwargs_modelticketmetamodel()

            with django_db_blocker.unblock():

                ticket_model_class =  apps.get_model(
                    app_label = model._meta.app_label,
                    model_name = str( model._meta.object_name )[0:len(model._meta.object_name)-6]
                )

                ticket_model = request.getfixturevalue(
                    # 'model_' + request.cls.ticket_model_class._meta.model_name
                    'model_' + ticket_model_class._meta.model_name
                )

                ticket_model_kwargs = request.getfixturevalue(
                    'kwargs_' + ticket_model._meta.model_name
                )()


                content_type = model_contenttype.objects.filter(
                    app_label = ticket_model._meta.app_label,
                    model = ticket_model._meta.model_name
                ).first()

                model_kwargs['content_type'] = content_type


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

                model_objs += [ model ]

                for key, value in kwargs_many_to_many.items():

                    field = getattr(model, key)

                    for entry in value:

                        field.add(entry)


            if ticket_model_class._meta.model_name == 'tenant':
                model_kwargs['organization'] = organization_one
                model_kwargs['model'] = organization_one

            else:

                model_kwargs.update({
                    'model': model
                })

            request.cls.kwargs_create_item = model_kwargs

            return model_kwargs

        yield factory

        with django_db_blocker.unblock():

            for obj in model_objs:
                obj.delete()



    @pytest.mark.regression
    def test_single_ticket_for_model(self, created_model, model):
        """Test row Unique
        
        Must only be able to assing a ticket to a model once.
        """

        with pytest.raises(ValidationError):

            model.objects.create(
                model = created_model.model,
                ticket = created_model.ticket
            )





for centurion_model in get_models(
                        excludes = [
                            'centurionaudit',
                            'history',
                            'centurionmodelnote',
                            'manufacturer',
                            'notes'
                        ]
):

    model_name = centurion_model._meta.model_name

    if(
        not issubclass(centurion_model, ModelTicketMetaModel)
        and not model_name.endswith('ticket')
        and not len(model_name) > 6
    ):
        continue

    cls_name: str = f"{centurion_model._meta.object_name}ModelPyTest"

    dynamic_class = type(
        cls_name,
        (ModelTicketMetaModelTestCases,),
        {
            '__module__': 'api.tests.functional.test_functional_meta_permissions_api',
            '__qualname__': cls_name,
            'model': make_fixture_with_args(
                arg_names = ['model_modelticketmetamodel' ],
                func = model,
                decorator_factory = pytest.fixture,
                decorator_args = {'scope': 'class'}

            ),
            'test_model': centurion_model,
        }
    )

    dynamic_class = pytest.mark.__getattr__('tickets')(dynamic_class)
    dynamic_class = pytest.mark.__getattr__(
        'module_'+centurion_model._meta.app_label
    )(dynamic_class)

    globals()[cls_name] = dynamic_class
