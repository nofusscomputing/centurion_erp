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


    kwargs_create_item = {
            'before': {},
            'after': {
                'after_key': 'after_value'
            },
            'action': CenturionAudit.Actions.ADD,
            'user': 'fixture sets value',
            'content_type': 'fixture sets value',
        }


    @pytest.fixture( scope = 'class', autouse = True )
    def setup_vars(self, content_type, django_db_blocker, user, model):

        with django_db_blocker.unblock():

            try:

                content_type = content_type.objects.get(
                    app_label = model._meta.app_label,
                    model = model._meta.model_name,
                )

            except content_type.DoesNotExist:
                # Enable Abstract models to be tested

                content_type = content_type.objects.get(
                    pk = 1,
                )


        self.kwargs_create_item.update({
            'content_type': content_type,
            'user': user,
        })



class CenturionAuditModelInheritedCases(
    CenturionAuditModelTestCases,
):

    pass
