from django.test import Client



class AdditionalTestCases:


    def test_permission_add(self, model_instance, api_request_permissions,
        model_kwargs, kwargs_api_create,
    ):
        client = Client()

        client.force_login( api_request_permissions['user']['add'] )


        kwargs = model_kwargs()
        kwargs.update({
            'organization': api_request_permissions['tenancy']['user']
        })

        the_model = model_instance( kwargs_create = kwargs )

        url = the_model.get_url( many = True )

        kwargs_create = kwargs_api_create.copy()
        kwargs_create['created_by'] = api_request_permissions['user']['add'].id
        kwargs_create['organization'] = api_request_permissions['tenancy']['user'].id


        response = client.post(
            path = url,
            data = kwargs_create,
            content_type = 'application/json'
        )


        assert response.status_code == 200, response.content
