import pytest

from centurion.tests.integration.test_integration_common import (
    IntegrationCommon
)

from core.mixins.centurion import Centurion



class AdditionalTestCases:


    @pytest.fixture( scope = 'class' )
    def api_request_permissions(self, api_request_permissions,
        model, model_kwargs, model_permission, model_contenttype,
    ):


        for action in ['add', 'change' ]:

            role_permissions = api_request_permissions['user'][action].groups.all(

            ).first().roles.first().permissions

            current_permission = role_permissions.first()


            for field_name, value in model_kwargs().items():

                    field_model = value.__class__

                    if(
                        field_name in [
                            'organization'
                        ]
                        or not issubclass(value.__class__, Centurion)
                        or (
                            current_permission.codename == f'{action}_{field_model._meta.model_name}'
                            and current_permission.content_type.app_label == field_model._meta.app_label
                        )
                    ):
                        continue



                    field_view_permission = model_permission.objects.get(
                        codename = 'view_' + field_model._meta.model_name,
                        content_type = model_contenttype.objects.get(
                            app_label = field_model._meta.app_label,
                            model = field_model._meta.model_name,
                        )
                    )

                    role_permissions.add( field_view_permission )


        yield api_request_permissions


    def test_backend_crud_create(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be created.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        model_relative_url = the_model.get_url( many = True )

        the_model.delete()

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


    def test_backend_crud_change(self,
        auto_login_client, api_request_permissions, model_kwargs,
        model_instance
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = change_item.get_url( many = False )


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        change_data = {}

        for key, value in model_kwargs().items():

            if(
                key in ['name', 'title', 'model_notes']
                and value not in [ None, '']
            ):

                change_data[key] = value

                break

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['change'],
            json = change_data,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "PATCH",
            url = url,
        )


        assert response.status_code == 200, response.content



    def test_backend_crud_delete(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        model_relative_url = delete_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['delete'],
            method = "DELETE",
            url = url,
        )


        assert response.status_code == 204, response.content



    def test_backend_crud_view(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = view_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['view'],
            method = "GET",
            url = url,
        )

        assert response.status_code == 200, response.content



    @pytest.mark.parametrize(
        argnames = "url_many",
        argvalues = [ True, False ],
        ids = [ 'list_view', 'detail_view'],
    )
    def test_backend_view_metdata(self,
        auto_login_client, api_request_permissions, url_many,
        model_instance, model_kwargs
    ):

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user'],
            'model': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        model_relative_url = view_item.get_url( many = url_many )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions['user']['view'],
            method = "GET",
            url = url,
        )

        assert response.status_code == 200, response.content
