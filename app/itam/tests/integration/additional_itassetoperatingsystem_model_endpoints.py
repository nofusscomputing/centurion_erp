import pytest

from centurion.tests.integration.test_integration_common import (
    IntegrationCommon
)



class AdditionalTestCases:


    @pytest.fixture( scope = 'class')
    def api_request_permissions_m2m(self, api_request_permissions,
        django_db_blocker, model_kwargs, model_permission,
        model_contenttype,
    ):


        with django_db_blocker.unblock():

            amended_request_permissions = api_request_permissions.copy()

            kwargs = model_kwargs()

            parent_model = kwargs['it_asset']

            change_permission = model_permission.objects.get(
                    codename = 'change_' + parent_model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = parent_model._meta.app_label,
                        model = parent_model._meta.model_name,
                    )
                )

            amended_request_permissions['user']['add'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            amended_request_permissions['user']['change'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            amended_request_permissions['user']['delete'].groups.all(
            ).first().roles.all().first().permissions.add(change_permission)

            view_permission = model_permission.objects.get(
                    codename = 'view_' + parent_model._meta.model_name,
                    content_type = model_contenttype.objects.get(
                        app_label = parent_model._meta.app_label,
                        model = parent_model._meta.model_name,
                    )
                )

            amended_request_permissions['user']['view'].groups.all(
            ).first().roles.all().first().permissions.add(view_permission)


        yield amended_request_permissions



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_backend_crud_create(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be created.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_backend_crud_change(self,
        auto_login_client, api_request_permissions, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be updated.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
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


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_backend_crud_delete(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be deleted.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    def test_backend_crud_view(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be viewed.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.regression
    @pytest.mark.xfail( reason = 'm2m models also require parent model view permissions' )
    @pytest.mark.parametrize(
        argnames = "url_many",
        argvalues = [ True, False ],
        ids = [ 'list_view', 'detail_view'],
    )
    def test_backend_view_metdata(self,
        auto_login_client, api_request_permissions,
        model_instance, model_kwargs, url_many
    ):
        """ Check Backend API 

        Ensure that the metadat for a model can be viewed.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
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



    def test_backend_crud_create_m2m_model(self,
        auto_login_client, api_request_permissions_m2m, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be created.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        model_relative_url = the_model.get_url( many = True )

        the_model.delete()

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['organization'] = api_request_permissions_m2m['tenancy']['user'].id


        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions_m2m['user']['add'],
            json = kwargs_create,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "POST",
            url = url,
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 201, response.content



    def test_backend_crud_change_m2m_model(self,
        auto_login_client, api_request_permissions_m2m, kwargs_api_create,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be updated.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
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
            re_login = api_request_permissions_m2m['user']['change'],
            json = change_data,
            headers = {
                'Content-Type': 'application/json'
            },
            method = "PATCH",
            url = url,
        )


        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    def test_backend_crud_delete_m2m_model(self,
        auto_login_client, api_request_permissions_m2m,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be deleted.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = delete_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions_m2m['user']['delete'],
            method = "DELETE",
            url = url,
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content



    def test_backend_crud_view_m2m_model(self,
        auto_login_client, api_request_permissions_m2m,
        model_instance, model_kwargs
    ):
        """ Check Backend API CRUD action 

        Ensure that a model can be viewed.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )


        model_relative_url = view_item.get_url( many = False )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions_m2m['user']['view'],
            method = "GET",
            url = url,
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content



    @pytest.mark.parametrize(
        argnames = "url_many",
        argvalues = [ True, False ],
        ids = [ 'list_view', 'detail_view'],
    )
    def test_backend_view_metdata_m2m_model(self,
        auto_login_client, api_request_permissions_m2m,
        model_instance, model_kwargs, url_many
    ):
        """ Check Backend API 

        Ensure that the metadat for a model can be viewed.
        """

        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions_m2m['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        model_relative_url = view_item.get_url( many = url_many )

        url = f"{IntegrationCommon.API_URL}{model_relative_url}"

        response = auto_login_client.request(
            auth = True,
            re_login = api_request_permissions_m2m['user']['view'],
            method = "GET",
            url = url,
        )

        assert response.status_code == 200, response.content
