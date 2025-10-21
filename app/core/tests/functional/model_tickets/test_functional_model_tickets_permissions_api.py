import pytest

from django.apps import apps
from django.conf import settings
from django.db import models
from django.test import Client
from django.utils.module_loading import import_string

from api.tests.functional.test_functional_permissions_api import (
    APIPermissionsInheritedCases
)

from core.models.model_tickets import ModelTicket, ModelTicketMetaModel



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


class APIPermissionsTestCases(
    APIPermissionsInheritedCases
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
        model, organization_one, clean_model_from_db
    ):

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

        def factory(
            model = model,
            ticket_model_class = ticket_model_class,
            ticket_model = ticket_model,
        ):

            model_kwargs = kwargs_modelticketmetamodel()

            with django_db_blocker.unblock():


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


            if ticket_model_class._meta.model_name == 'tenant':
                model_kwargs['organization'] = organization_one
                model_kwargs['model'] = organization_one

            else:

                model_kwargs.update({
                    'model': model
                })

            request.cls.kwargs_create_item.update(model_kwargs)

            return model_kwargs

        yield factory

        clean_model_from_db(ticket_model)

        clean_model_from_db(ticket_model_class)

        clean_model_from_db(model)



    def test_permission_add(self, model, api_request_permissions,
        model_kwargs, kwargs_api_create, model_instance,
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        kwargs = model_kwargs()
        kwargs['model'] = model.model.field.related_model.objects.get(
            pk = kwargs_api_create['model']
        )

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        the_model.delete()

        response = client.post(
            path = url,
            data = kwargs_api_create,
            content_type = 'application/json'
        )

        assert response.status_code == 201, response.content



    def test_returned_results_only_user_orgs(self):
        pytest.xfail( reason = 'this model is not filterable to org, it is by ticket or model' )

    def test_returned_data_from_user_and_global_organizations_only(self):
        pytest.xfail( reason = 'this model is not filterable to org, it is by ticket or model' )






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

    cls_name: str = f"{centurion_model._meta.object_name}APIPermissionsPyTest"

    inc_classes = (APIPermissionsTestCases,)
    try:

        additional_testcases = import_string(
            centurion_model._meta.app_label + '.tests.functional.additional_' +
            centurion_model._meta.model_name + '_permissions_api.AdditionalTestCases'
        )

        inc_classes = (additional_testcases, *inc_classes)

    except Exception as ex:
        additional_testcases = None

    dynamic_class = type(
        cls_name,
        inc_classes,
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
