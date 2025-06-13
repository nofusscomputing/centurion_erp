from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = 'Return a list of All Centurion Models.'


    def get_models(self, excludes: list[ str ] = [] ) -> list[ tuple ]:
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


    def add_arguments(self, parser):
        parser.add_argument('-e', '--exclude', action='store',
        help='CSV list of models to exclude. Case Insensitive and partial match.')


    def handle(self, *args, **kwargs):

        excludes = []

        if kwargs.get('exclude', None):

            vals = str(kwargs['exclude']).split(',')

            for model in vals:
                excludes += [ model ]


        models = self.get_models( excludes = excludes )
        models.sort(key = lambda x: f'{x._meta.app_label}.{x._meta.object_name}')

        for model in models:

            print(f'{model._meta.app_label}.{model._meta.object_name}')