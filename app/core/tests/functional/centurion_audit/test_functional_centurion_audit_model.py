import pytest

from django.apps import apps
from django.conf import settings

from core.models.audit import CenturionAudit

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)


@pytest.mark.audit_models
class CenturionAuditModelTestCases(
    CenturionAbstractModelInheritedCases
):



    @pytest.fixture( scope = 'class', autouse = True )
    def setup_vars(self, model_contenttype, django_db_blocker, model):

        with django_db_blocker.unblock():

            try:

                content_type = model_contenttype.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )

            except content_type.DoesNotExist:
                # Enable Abstract models to be tested

                content_type = model_contenttype.objects.get(
                    pk = 1,
                )


        self.kwargs_create_item.update({
            'content_type': content_type,
        })



class CenturionAuditModelInheritedCases(
    CenturionAuditModelTestCases,
):

    pass



class CenturionAuditModelPyTest(
    CenturionAuditModelTestCases,
):



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



    history_models = get_models( [ 'audithistory', 'base', 'history', 'note', 'ticket' ] )


    @pytest.mark.parametrize(
        argnames = [
            'test_model'
        ],
        argvalues = history_models,
        ids = [ model[0]._meta.app_label + '_' + model[0]._meta.model_name for model in history_models ]
    )
    def test_model_has_history_model(self, test_model, model):
        """Audit History Table check

        Check if the model has a corresponding audit history table that should be
        called `<app_label>_<model_name>_audithistory`
        """

        if test_model._meta.abstract:

            pytest.xfail( reason = 'Model is an Abstract Model and can not be created.' )

        elif not getattr(test_model, '_audit_enabled', False):

            pytest.xfail( reason = 'Model has audit history disabled.' )


        history_model = apps.get_model(
            app_label = test_model._meta.app_label,
            model_name = test_model().get_history_model_name()
        )

        assert history_model.__name__ == test_model().get_history_model_name()
