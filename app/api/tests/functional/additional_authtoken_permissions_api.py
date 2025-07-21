import pytest
# import random

from django.test import Client
from django.urls.exceptions import NoReverseMatch

# from rest_framework.permissions import (
#     IsAuthenticatedOrReadOnly
# )



class AdditionalTestCases:


    def test_permission_add(self, mocker,
        model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create
    ):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['add'] )

        the_model = model_instance( kwargs_create = self.kwargs_create_item )

        context_user = mocker.patch.object(
            the_model, 'context'
        )

        context_user.__getitem__.side_effect = {
            'logger': None,
            'user': api_request_permissions['user']['add']
        }.__getitem__

        the_model.user = api_request_permissions['user']['add']


        url = the_model.get_url( many = True )

        # the_model.delete()

        response = client.post(
            path = url,
            data = kwargs_api_create,
            content_type = 'application/json'
        )

        assert response.status_code == 201, response.content



    def test_permission_delete(self, mocker, model_instance, api_request_permissions):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['delete'] )

        kwargs = self.kwargs_create_item
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        delete_item = model_instance(
            kwargs_create = kwargs
        )

        context_user = mocker.patch.object(
            delete_item, 'context'
        )

        context_user.__getitem__.side_effect = {
            'logger': None,
            'user': api_request_permissions['user']['delete']
        }.__getitem__

        delete_item.user = api_request_permissions['user']['delete']


        response = client.delete(
            path = delete_item.get_url( many = False ),
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 204, response.content



    def test_permission_view(self, mocker, model_instance, api_request_permissions):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['view'] )

        kwargs = self.kwargs_create_item
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        view_item = model_instance(
            kwargs_create = kwargs
        )

        context_user = mocker.patch.object(
            view_item, 'context'
        )

        context_user.__getitem__.side_effect = {
            'logger': None,
            'user': api_request_permissions['user']['view']
        }.__getitem__

        view_item.user = api_request_permissions['user']['view']


        response = client.get(
            path = view_item.get_url( many = False )
        )

        if response.status_code == 405:
            pytest.xfail( reason = 'ViewSet does not have this request method.' )

        assert response.status_code == 200, response.content




    def test_returned_results_only_user_orgs(self):
        pytest.mark.xfail( reason = 'This model is not tenancy based. It is user based.' )

    def test_returned_data_from_user_and_global_organizations_only(self):
        pytest.mark.xfail( reason = 'This model is not tenancy based. It is user based.' )
