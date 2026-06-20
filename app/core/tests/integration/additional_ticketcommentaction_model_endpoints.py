import pytest

from centurion.tests.integration.test_integration_common import (
    IntegrationCommon
)



class AdditionalTestCases:


    @pytest.mark.xfail( reason = 'Only an import user can create this model.' )
    def test_backend_crud_create(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs, model_contenttype
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )


        model_relative_url = the_model.get_url( many = True )

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['add'],
            json = kwargs_create,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "POST",
            url = url,
        )


        assert response.status_code == 201, response.content



    def test_backend_crud_create_import_permission(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs, model_contenttype
    ):
        """ Test Create endpoint

        An import user must be able to create this model.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )


        user_role = api_request_permissions['user']['add'].groups.all(
        )[0].roles.all()[0]

        import_permission = model_contenttype.objects.get_for_model(
            the_model.__class__
        ).permission_set.get(
            codename = f"import_{the_model.__class__._meta.model_name}"
        )

        user_role.permissions.add(import_permission)


        model_relative_url = the_model.get_url( many = True )

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['add'],
            json = kwargs_create,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "POST",
            url = url,
        )


        assert response.status_code == 201, response.content
