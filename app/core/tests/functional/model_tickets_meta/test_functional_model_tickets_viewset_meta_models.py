import pytest
import random

from django.apps import apps
from django.conf import settings
from django.db import models

from api.tests.functional.test_functional_common_viewset import (
    MockRequest
)

from core.models.model_tickets import ModelTicketMetaModel
from core.tests.functional.model_tickets.test_functional_model_tickets_viewset import (
    ModelTicketViewsetInheritedCases
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


class ModelTicketMetaViewsetTestCases(
    ModelTicketViewsetInheritedCases
):
    """API Permission Test Cases

    This test suite is dynamically created for `Centurion` sub-classes.
    Each `Centurion` must ensure their model fixture exists in
    `tests/fixtures/model_<model_name>` with fixtures `model_<model_name>` and
    `kwargs_<model_name>` defined.
    """


    @pytest.fixture( scope = 'class', autouse = True)
    def model_kwargs(self, django_db_blocker,
        clean_model_from_db,
        request, kwargs_modelticketmetamodel, model_contenttype,
        model, organization_one,
    ):

        if not hasattr(request.cls, 'kwargs_create_item'):
            request.cls.kwargs_create_item = {}

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
            )

        model_obj = []
        def factory(
            ticket_model_class = ticket_model_class,
            ticket_model = ticket_model,
            ticket_model_kwargs = ticket_model_kwargs,
            organization = None
        ):

            model_kwargs = kwargs_modelticketmetamodel()

            with django_db_blocker.unblock():

                kwargs_many_to_many = {}

                kwargs = {}

                for key, value in ticket_model_kwargs().items():

                    field = ticket_model._meta.get_field(key)

                    if isinstance(field, models.ManyToManyField):

                        kwargs_many_to_many.update({
                            key: value
                        })

                    else:

                        kwargs.update({
                            key: value
                        })


                if organization:
                    kwargs['organization'] = organization

                if ticket_model._meta.model_name == 'tenant':
                    obj = organization

                else:

                    obj = ticket_model.objects.create( **kwargs )

                for key, value in kwargs_many_to_many.items():

                    field = getattr(obj, key)

                    for entry in value:

                        field.add(entry)


            if ticket_model_class._meta.model_name == 'tenant':
                model_kwargs['organization'] = organization_one
                model_kwargs['model'] = organization_one

            else:

                model_kwargs.update({
                    'model': obj
                })

            request.cls.kwargs_create_item.update(model_kwargs)

            return model_kwargs

        yield factory

        clean_model_from_db(model)
        clean_model_from_db(ticket_model_class)
        clean_model_from_db(ticket_model)


    @pytest.fixture( scope = 'function' )
    def viewset_mock_request(self, django_db_blocker, viewset,
        clean_model_from_db, api_request_permissions,
        model_user, kwargs_user, organization_one, organization_two,
        model_instance, model_kwargs, model, model_ticketcommentbase,
        kwargs_ticketbase,
    ):

        with django_db_blocker.unblock():

            user = api_request_permissions['user']['view']

            kwargs = kwargs_user()
            kwargs['username'] = 'username.two' + str(
                random.randint(1,99) + random.randint(1,99) + random.randint(1,99) )
            user2 = model_user.objects.create( **kwargs )

            self.user = user

            kwargs = model_kwargs()
            kwargs['organization'] = organization_one

            if kwargs['model']._meta.model_name == 'tenant':
                kwargs['model'] = organization_one

            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user2

            user_tenancy_item = model_instance( kwargs_create = kwargs )

            kwargs = model_kwargs( organization = organization_two)

            kwargs_ticket = kwargs_ticketbase()
            kwargs_ticket['title'] = 'other org ticket'
            kwargs_ticket['organization'] = organization_two

            kwargs['ticket'] = kwargs['ticket'].__class__.objects.create(
                **kwargs_ticket
            )

            kwargs['organization'] = organization_two


            if(
                kwargs['model']._meta.model_name in [
                    'gitrepository',
                    'githubrepository',
                    'gitlabrepository',
                ]
            ):

                kwargs['model'].git_group.organization = organization_two

            elif hasattr(kwargs['model'], 'organization'):

                kwargs['model'].organization = organization_two

            elif kwargs['model']._meta.model_name == 'tenant':

                kwargs['model'] = organization_two


            kwargs['model'].save()

            if 'user' in kwargs and not issubclass(model, model_ticketcommentbase):
                kwargs['user'] = user


            other_tenancy_item = model_instance( kwargs_create = kwargs )


        view_set = viewset()

        request = MockRequest(
            user = user,
            model = model,
            viewset = viewset,
            tenant = organization_one
        )

        view_set.request = request
        view_set.kwargs = user_tenancy_item.get_url_kwargs( many = True )


        yield view_set

        del view_set.request
        del view_set
        del self.user

        clean_model_from_db(model)
        clean_model_from_db(model_user)
        clean_model_from_db(user_tenancy_item.__class__)
        clean_model_from_db(kwargs['model'].__class__)
        clean_model_from_db(kwargs['ticket'].__class__)



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
        (ModelTicketMetaViewsetTestCases,),
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
