import pytest

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


from access.tests.unit.managers.test_unit_common_manager import (
    CommonManagerInheritedCases
)
from access.tests.unit.managers.test_unit_tenancy_manager import (
    has_arg_kwarg
)



@pytest.mark.manager
@pytest.mark.manager_tenancy
class UserManagerTestCases(
    CommonManagerInheritedCases
):


    def test_manager_user_filter_user(self, mocker,
        model_instance, model, api_request_permissions
    ):

        filter = mocker.spy(models.QuerySet, 'filter')

        obj = model_instance

        if hasattr(model, 'organization'):
            obj.organization = api_request_permissions['tenancy']['user']
            obj.save()

        filter.reset_mock()

        model.objects.user(
            user = api_request_permissions['user']['view'],
            permission = str( model._meta.app_label + '.view_' + model._meta.model_name )
        ).all()

        assert any(
            has_arg_kwarg(call = c, key = 'user')
            and c.args[0].model is model for c in filter.call_args_list
        )





class UserManagerInheritedCases(
    UserManagerTestCases
):
    pass


@pytest.mark.module_access
class UserManagerPytest(
    UserManagerTestCases
):
    def test_manager_user_filter_user(self):
        pytest.xfail( reason = 'base model, test is n/a.' )
