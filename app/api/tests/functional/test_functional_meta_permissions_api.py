import pytest

from django.apps import apps
from django.conf import settings

from api.tests.functional.test_functional_permissions_api import (
    APIPermissionsInheritedCases
)

from core.mixins.centurion import Centurion



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

        if model._meta.app_label not in model_apps:
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

    yield model__model_name


def model_kwargs(self, request, kwargs__model_name):

    request.cls.kwargs_create_item = kwargs__model_name.copy()

    yield kwargs__model_name.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


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
    pass


for centurion_model in get_models(
                        excludes = [
                            'centurionaudit',
                            'history',
                            'centurionmodelnote',
                            'notes'
                        ]
):

    if(
        not issubclass(centurion_model, Centurion)
        or centurion_model == Centurion
        or centurion_model._meta.object_name in exclude_model_from_test
    ):
        continue

    model_name = centurion_model._meta.model_name
    cls_name: str = f"{centurion_model._meta.object_name}APIPermissionsPyTest"

    dynamic_class = type(
        cls_name,
        (APIPermissionsTestCases,),
        {
            '__module__': 'api.tests.functional.test_functional_meta_permissions_api',
            '__qualname__': cls_name,
            'model': make_fixture_with_args(
                arg_names = ['model_' + str(centurion_model._meta.model_name) ],
                func = model,
                decorator_factory = pytest.fixture,
                decorator_args = {'scope': 'class'}

            ),
            'model_kwargs': make_fixture_with_args(
                arg_names = ['request', f'kwargs_{model_name}' ],
                func = model_kwargs,
                decorator_factory = pytest.fixture,
                decorator_args = {'scope': 'class', 'autouse': True}
            )
        }
    )

    model_mark = f'model_{model_name}'
    dynamic_class = pytest.mark.__getattr__(model_mark)(dynamic_class)
    dynamic_class = pytest.mark.__getattr__('module_'+centurion_model._meta.app_label)(dynamic_class)

    globals()[cls_name] = dynamic_class
