from django.apps import apps
from django.conf import settings



def get_models(
    excludes: list[ str ] = [],
    excludes_model_classes: list = [],
    only_class = None
) -> list:
    """Fetch models from Centurion Apps

    Args:
        excludes (list[ str ]): Words that may be in a models name to exclude

    Returns:
        list[ tuple ]: Centurion ERP Only models
    """

    if only_class is None:
        only_class = type(only_class)

    excludes = [ str(model_name).lower() for model_name in excludes ]


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
            or (
                not issubclass(model, only_class)
                and only_class is not type(None)
            )
            or getattr(model, 'decorator_depreciated', False)
        ):
            continue

        skip = False

        if excludes_model_classes and only_class is type(None):

            for excluded_class in excludes_model_classes:

                if issubclass(model, excluded_class):
                    skip = True
                    break


        for exclude in excludes:

            if exclude in model_name:
                skip = True
                break

        if skip:
                continue

        models += [ model ]

    return models
