import pytest

from django.apps import apps
from django.conf import settings

from centurion.tests.helpers import get_models

from core.models.audit import CenturionAudit
from core.models.centurion_notes import CenturionModelNote
from core.models.model_tickets import ModelTicket



class MetaChecksPyTest:


    notes_models = [(model,) for model in get_models(
        excludes = [ 'base', ],
        excludes_model_classes = [
            CenturionAudit,
            CenturionModelNote,
            ModelTicket
        ]
    )]


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

        notes_model_table: str = test_model._meta.app_label + '_' + test_model._meta.model_name + '_centurionmodelnote'

        found = False

        for model in apps.get_models():

            if model._meta.db_table == notes_model_table:

                found = True
                break


        assert found



    # history_models = get_models( [ 'audithistory', 'base', 'history', 'note', 'ticket' ] )

    history_models = [(model,) for model in get_models(
        excludes = [ 'base', ],
        excludes_model_classes = [
            CenturionAudit,
            CenturionModelNote,
            ModelTicket
        ]
    )]


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

        history_model_table: str = test_model._meta.app_label + '_' + test_model._meta.model_name + '_audithistory'

        found = False

        for model in apps.get_models():

            if model._meta.db_table == history_model_table:

                found = True
                break


        assert found
