import pytest

from django.apps import apps

from access.tests.functional.tenancy_abstract.test_functional_tenancy_abstract_model import (
    TenancyAbstractModelInheritedCases
)



@pytest.mark.centurion_models
class CenturionAbstractModelTestCases(
    TenancyAbstractModelInheritedCases
):


    kwargs_create_item = {
            'model_notes': 'model notes txt',
            'created': '2025-05-23T00:00',
        }



    def test_model_has_history_model(self, model):
        """Audit History Table check

        Check if the model has a corresponding audit history table that should be
        called `<app_label>_<model_name>_audithistory`
        """

        if model._meta.abstract:

            pytest.xfail( reason = 'Model is an Abstract Model and can not be created.' )

        elif not getattr(model, '_audit_enabled', False):

            pytest.xfail( reason = 'Model has audit history disabled.' )


        history_model = apps.get_model(
            app_label = model._meta.app_label,
            model_name = model().get_history_model_name()
        )

        assert history_model.__name__ == model().get_history_model_name()



    def test_model_create_has_history_entry(self, content_type, created_model, model):
        """Model Created

        Ensure that the model when created, added a `create` Audit History
        entry.
        """

        if model._meta.abstract:

            pytest.xfail( reason = 'Model is an Abstract Model and can not be created.' )

        elif not getattr(model, '_audit_enabled', False):

            pytest.xfail( reason = 'Model has audit history disabled.' )


        history_model = apps.get_model( created_model._meta.app_label, created_model.get_history_model_name() )

        entry = history_model.objects.get(
            model = created_model,
            content_type = content_type.objects.get(
                app_label = created_model._meta.app_label,
                model = created_model._meta.model_name
            )
        )

        assert entry.model == created_model



class CenturionAbstractModelInheritedCases(
    CenturionAbstractModelTestCases,
):
    pass



class CenturionAbstractModelPyTest(
    CenturionAbstractModelTestCases,
):

    pass
