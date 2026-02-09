import pytest
import random

from django.test import Client

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from centurion_feature_flag.lib.feature_flag import CenturionFeatureFlagging



class AdditionalTestCases:


    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create,
        model_permission, model_contenttype,
        model_employee, kwargs_employee,
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        kwargs = kwargs_employee()
        kwargs['user'] = api_request_permissions['user']['add']
        emplyoee = model_employee.objects.create( **kwargs )



        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        triage_permissions = model_permission.objects.get(
                codename = 'triage_' + the_model.ticket._meta.model_name,
                content_type = model_contenttype.objects.get(
                    app_label = the_model.ticket._meta.app_label,
                    model = the_model.ticket._meta.model_name,
                )
            )

        api_request_permissions['user']['add'].groups.all(
        ).first().roles.all().first().permissions.add(triage_permissions)



        client.force_login( api_request_permissions['user']['add'] )


        url = the_model.get_url( many = True )

        # the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        # kwargs_create['model'] = the_model.model.id
        kwargs_create['created_by'] = api_request_permissions['user']['add'].id
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        try:

            response = client.post(
                path = url,
                data = kwargs_create,
                content_type = 'application/json'
            )

        except NoReverseMatch:

            # Cater for models that use viewset `-list` but `-detail`
            try:

                response = client.post(
                    path = the_model.get_url( many = False ),
                    data = kwargs_create
                )

            except NoReverseMatch:

                pass


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



    def test_permission_change(self, model_instance, api_request_permissions, model_kwargs,
        model_employee, kwargs_employee,
    ):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        kwargs = kwargs_employee()
        kwargs['user'] = api_request_permissions['user']['change']
        emplyoee = model_employee.objects.create( **kwargs )

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = self.change_data,
            content_type = 'application/json'
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content
