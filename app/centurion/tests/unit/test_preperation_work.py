import pytest

from django.apps import apps
from django.conf import settings


class MetaChecksPyTest:

    @staticmethod
    def get_models( excludes: list[ str ] ) -> list[ tuple ]:
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

            models += [ (model,) ]

        return models



    notes_models = get_models( [ 'base', 'history', 'note', 'ticket' ] )


    @pytest.mark.xfail( reason = 'Test Checks if installed models has a notes table' )
    @pytest.mark.parametrize(
        argnames = [
            'test_model'
        ],
        argvalues = notes_models,
        ids = [ model[0]._meta.app_label + '_' + model[0]._meta.model_name for model in notes_models ]
    )
    def test_model_has_notes(self, test_model):
        """Note Table check

        Check if the model has a corresponding notes table that should be
        called `<app_label>_<model_name>_notes`
        """

        notes_model_table: str = test_model._meta.app_label + '_' + test_model._meta.model_name + '_notes'

        found = False

        for model in apps.get_models():

            if model._meta.db_table == notes_model_table:

                found = True
                break


        assert found



    history_models = get_models( [ 'base', 'history', 'note', 'ticket' ] )


    @pytest.mark.xfail( reason = 'Test Checks if installed models has a History table' )
    @pytest.mark.parametrize(
        argnames = [
            'test_model'
        ],
        argvalues = history_models,
        ids = [ model[0]._meta.app_label + '_' + model[0]._meta.model_name for model in history_models ]
    )
    def test_model_has_history(self, test_model):
        """History Table check

        Check if the model has a corresponding notes table that should be
        called `<app_label>_<model_name>_notes`
        """

        history_model_table: str = test_model._meta.app_label + '_' + test_model._meta.model_name + '_history'

        found = False

        for model in apps.get_models():

            if model._meta.db_table == history_model_table:

                found = True
                break


        assert found
