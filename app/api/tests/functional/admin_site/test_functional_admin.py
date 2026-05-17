import pytest

from django.test import Client



@pytest.mark.functional
@pytest.mark.module_api
class AdminSitePyTest:

    admin_endpoint: str = '/admin/'


    def test_endpoint_admin_not_staff_user_cant_access(self, api_request_permissions):
        """Admin Panel

        Confirm that user whom marked as `super_user` can access the admin
        endpoint.
        """

        api_request_permissions['user']['view'].is_staff = False
        api_request_permissions['user']['view'].save()

        assert not api_request_permissions['user']['view'].is_staff, "User must not be a staff for the test to work"


        client = Client()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.get( path = self.admin_endpoint )

        assert (
            response.status_code == 302
            and '/login/' in response.url
        )



    def test_endpoint_admin_staff_user_can_access(self, api_request_permissions):
        """Admin Panel

        Confirm that user whom marked as `super_user` can access the admin
        endpoint.
        """

        api_request_permissions['user']['view'].is_staff = True
        # api_request_permissions['user']['view'].is_superuser = True
        api_request_permissions['user']['view'].save()

        assert api_request_permissions['user']['view'].is_staff, "User must be a staff for the test to work"


        client = Client()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.get( path = self.admin_endpoint )

        assert response.status_code == 200



    def test_endpoint_admin_super_user_can_access(self, api_request_permissions):
        """Admin Panel

        Confirm that user whom marked as `super_user` can access the admin
        endpoint.
        """

        api_request_permissions['user']['view'].is_staff = True
        api_request_permissions['user']['view'].is_superuser = True
        api_request_permissions['user']['view'].save()


        assert api_request_permissions['user']['view'].is_staff, "User must be a staff for the test to work"
        assert api_request_permissions['user']['view'].is_superuser, "User must be a superuser for the test to work"


        client = Client()

        client.force_login( api_request_permissions['user']['view'] )
        response = client.get( path = self.admin_endpoint )

        assert response.status_code == 200
