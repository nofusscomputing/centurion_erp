import pytest

from django.db import models

from access.tests.unit.managers.test_unit_tenancy_manager import (
    has_arg_kwarg,
    TenancyManagerInheritedCases
)

from core.tests.unit.mixin_centurion.test_unit_centurion_mixin import (
    CenturionMixnInheritedCases,
)


@pytest.mark.module_access
@pytest.mark.model_tenant
class TenantModelTestCases(
    TenancyManagerInheritedCases,
    CenturionMixnInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'tenant'
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'id': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.AutoField,
            'null': False,
            'unique': True,
        },
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'max_length': 50,
            'null': False,
            'unique': True,
        },
        'manager': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'model_notes': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': True,
            'unique': False,
        },
        'created': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': False,
            'unique': False,
        },
        'modified': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': False,
            'unique': False,
        },
    }


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
            has_arg_kwarg(call = c, key = 'id__in') 
            and c.args[0].model is model for c in filter.call_args_list
        )

    def test_manager_tenancy_select_related(self):
        pytest.xfail( reason = 'Model is the Tenant model, cant select itself.' )



class TenantModelInheritedCases(
    TenantModelTestCases,
):
    pass



class TenantModelPyTest(
    TenantModelTestCases,
):
    pass
