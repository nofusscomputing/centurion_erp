import pytest

from django.test import Client



class AdditionalTestCases:


    def test_permission_change(self, model_instance, api_request_permissions, model_kwargs):
        """ Check correct permission for change

        Make change with user who has change permission
        """

        client = Client()

        client.force_login( api_request_permissions['user']['change'] )

        kwargs = model_kwargs.copy()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        change_item = model_instance(
            kwargs_create = kwargs,
        )

        kwargs = self.change_data.copy()
        kwargs.update({ 'name': 'changed d'})

        response = client.patch(
            path = change_item.get_url( many = False ),
            data = kwargs,
            content_type = 'application/json'
        )

        assert response.status_code == 200, response.content
