import pytest

from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


from access.tests.unit.managers.test_unit_common_manager import (
    CommonManagerInheritedCases
)



def has_arg_kwarg(call, key):
    args, kwargs = call

    for arg in args:
        if isinstance(arg, Q):
            for (k, v) in arg.children:
                if k == key:
                    return True
        if arg == key:
            return True

    # check direct kwargs
    if key in kwargs:
        return True

    return False



@pytest.mark.manager
@pytest.mark.manager_tenancy
class TenancyManagerTestCases(
    CommonManagerInheritedCases
):


    def test_manager_tenancy_filter_tenant(self, mocker,
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
            has_arg_kwarg(call = c, key = 'organization__in') 
            and c.args[0].model is model for c in filter.call_args_list
        )


    def test_manager_tenancy_select_related(self, mocker,
        model_instance, model, api_request_permissions
    ):

        select_related = mocker.spy(QuerySet, "select_related")

        select_related.reset_mock()

        model.objects.user(
            user = api_request_permissions["user"]["view"],
            permission = f"{model._meta.app_label}.view_{model._meta.model_name}",
        ).all()

        assert any(
            has_arg_kwarg(call = c, key = 'organization')
            and c.args[0].model is model for c in select_related.call_args_list
        )




class TenancyManagerInheritedCases(
    TenancyManagerTestCases
):
    pass


@pytest.mark.module_access
class TenancyManagerPytest(
    TenancyManagerTestCases
):
    def test_manager_tenancy_filter_tenant(self):
        pytest.xfail( reason = 'base model, test is n/a.' )

    def test_manager_tenancy_select_related(self):
        pytest.xfail( reason = 'base model, test is n/a.' )
