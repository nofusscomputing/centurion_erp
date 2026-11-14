import pytest

from django.apps import apps
from django.conf import settings

from centurion.tests.helpers import get_models

from core.models.audit import CenturionAudit
from core.models.centurion_notes import CenturionModelNote
from core.models.model_tickets import ModelTicket

from core.tests.functional.centurion_abstract.test_functional_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)


@pytest.mark.audit_models
class CenturionAuditModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
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



    history_models = [(model,) for model in get_models(
        excludes = [ 'base', 'manufacturer', 'team', 'teamusers' ],
        excludes_model_classes = [
            CenturionAudit,
            CenturionModelNote,
            ModelTicket
        ]
    )]


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
