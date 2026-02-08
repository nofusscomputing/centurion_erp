import pytest
import random

from django.test import Client



class AdditionalTestCases:


    def test_manager_filter_content_has_perm(self, model,
        model_kwargs, model_permission, model_contenttype,
        organization_one, organization_two,
        model_employee, kwargs_employee,
        model_role
    ):
        """Model Manager Test

        Confirm that the model manager only filters to those the user has
        access to.
        """

        employee = model_employee.objects.create( **kwargs_employee() )


        view_permission = model_permission.objects.get(
            codename = 'view_' + model._meta.model_name,
            content_type = model_contenttype.objects.get(
                app_label = model._meta.app_label,
                model = model._meta.model_name,
            )
        )

        view_role = model_role.objects.create(
            organization = organization_one,
            name = 'add_role' + str( random.randint(1,999) ) + str( random.randint(1,999) ),
        )

        view_role.users.set( [ employee.user ] )
        view_role.permissions.set( [ view_permission ] )

        # Create Other org item
        kwargs = model_kwargs()

        kwargs['model'] = organization_two

        diff_org_item = model.objects.create( **kwargs )

        queryset = model.objects.user(
            user = employee.user,
            permission = [ f'{view_permission.content_type.app_label}.{view_permission.codename}' ]
        ).all()

        assert diff_org_item.organization == organization_two, 'For the test to function two objects in different tenancies must exist'

        for found_model in queryset:

            assert found_model.organization == organization_one, (
                f'model {found_model} was not filtered out. organization={found_model.organization}'
            )



    def test_manager_filter_content_no_perm(self, model,
        model_kwargs, model_permission, model_contenttype,
        organization_two,
        model_employee, kwargs_employee,
        model_role, model_configgroups, kwargs_configgroups
    ):
        """Model Manager Test

        Confirm that the model manager only filters to those the user has
        access to.
        """

        employee = model_employee.objects.create( **kwargs_employee() )


        view_permission = model_permission.objects.get(
            codename = 'view_' + model._meta.model_name,
            content_type = model_contenttype.objects.get(
                app_label = model._meta.app_label,
                model = model._meta.model_name,
            )
        )

        # Create Other org item
        kwargs = model_kwargs()

        kwargs['model'] = organization_two
        diff_org_item = model.objects.create( **kwargs )

        queryset = model.objects.user(
            user = employee.user,
            permission = [ f'{view_permission.content_type.app_label}.{view_permission.codename}' ]
        ).all()

        assert diff_org_item.organization == organization_two, 'For the test to function two objects in different tenancies must exist'


        assert len(queryset) == 0, f'No objects should have returned, {queryset}'
