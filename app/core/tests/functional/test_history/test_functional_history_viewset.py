import django

from django.contrib.auth.models import ContentType, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_permissions_viewset import APIPermissionView
from api.tests.abstract.test_metadata_functional import (
    MetadataAttributesFunctionalBase,
    MetadataAttributesFunctionalEndpoint,
)

from core.models.model_history import ModelHistory

from itam.models.device import Device
from itam.models.device_history import DeviceHistory

from settings.models.app_settings import AppSettings

User = django.contrib.auth.get_user_model()



class ViewSetBase:

    model = ModelHistory

    app_namespace = 'v2'
    
    url_name = '_api_v2_model_history'

    change_data = {'name': 'device'}

    delete_data = {}

    @classmethod
    def setUpTestData(self):
        """Setup Test

        note: permissions set to use device history


        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        self.different_organization = Organization.objects.create(name='test_different_organization')

        self.global_organization = Organization.objects.create(
            name = 'test_global_organization'
        )

        self.other_org_item = Device.objects.create(
            organization = self.different_organization,
            name = 'two'
        )

        self.global_org_item = Device.objects.create(
            organization = self.global_organization,
            name = 'global_item'
        )

        app_settings = AppSettings.objects.get(
            owner_organization = None
        )

        app_settings.global_organization = self.global_organization

        app_settings.save()


        self.device = Device.objects.create(
            organization = self.organization,
            name = 'history-device'
        )



        view_permissions = Permission.objects.get(
                codename = 'view_' + DeviceHistory._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = DeviceHistory._meta.app_label,
                    model = DeviceHistory._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_' + DeviceHistory._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = DeviceHistory._meta.app_label,
                    model = DeviceHistory._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])



        change_permissions = Permission.objects.get(
                codename = 'change_' + DeviceHistory._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = DeviceHistory._meta.app_label,
                    model = DeviceHistory._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + DeviceHistory._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = DeviceHistory._meta.app_label,
                    model = DeviceHistory._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = organization,
        )

        delete_team.permissions.set([delete_permissions])


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        self.item = self.model.objects.filter(
            content_type = ContentType.objects.get(
                app_label = self.device._meta.app_label,
                model = self.device._meta.model_name
            )
        )[0]


        self.url_kwargs = {
            'app_label': self.device._meta.app_label,
            'model_name': self.device._meta.model_name,
            'model_id': self.device.id,
        }

        self.url_view_kwargs = {
            'app_label': self.device._meta.app_label,
            'model_name': self.device._meta.model_name,
            'model_id': self.device.id,
            'pk': self.item.pk
        }

        self.add_data = {}


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = self.different_organization,
        )

        different_organization_team.permissions.set([
            view_permissions,
            add_permissions,
            change_permissions,
            delete_permissions,
        ])

        TeamUsers.objects.create(
            team = different_organization_team,
            user = self.different_organization_user
        )



class HistoryPermissionsAPI(
    ViewSetBase,
    APIPermissionView,
    TestCase
):


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        Although this model is a tenancy model, the viewset filters by object
        ID, so will only return the one item.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_kwargs)


        only_from_user_org: bool = True

        viewable_organizations = [
            self.organization.id,
            self.global_organization.id
        ]


        assert getattr(self.global_organization, 'id', False)    # fail if no global org set
        assert getattr(self.global_org_item, 'id', False)    # fail if no global item set


        client.force_login(self.view_user)
        response = client.get(url)

        assert len(response.data['results']) == 1    # fail if only one item extist.



    def test_view_list_has_permission(self):
        """ Check correct permission for view

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs=self.url_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200


    def test_view_has_permission(self):
        """ Check correct permission for view

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Attempt to view as user with view permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        assert response.status_code == 200


    def test_add_has_permission_method_not_allowed(self):
        """ Check correct permission for add 

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Attempt to add as user with permission
        """

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 405



    def test_change_has_permission_method_not_allowed(self):
        """ Check correct permission for change

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Make change with user who has change permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.change_user)
        response = client.patch(url, data=self.change_data, content_type='application/json')

        assert response.status_code == 405


    def test_delete_has_permission_method_not_allowed(self):
        """ Check correct permission for delete

        Custom permission of test case with same name.
        This test ensures that the user is denied

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405



class HistoryMetadata(
    ViewSetBase,
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
    TestCase
):




    def test_method_options_request_detail_data_has_key_urls_self(self):
        """Test HTTP/Options Method

        This is a custom test of a test with the same name.
        history view has no detail view, due to using a custom
        view "history",

        Ensure the request data returned has key `urls.self`
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-list',
                kwargs=self.url_kwargs
            ),
            content_type='application/json'
        )

        assert 'urls' in response.data


    def test_method_options_request_detail_data_key_urls_self_is_str(self):
        """Test HTTP/Options Method

        This is a custom test of a test with the same name.
        history view has no detail view, due to using a custom
        view "history",

        Ensure the request data key `urls.self` is a string
        """

        client = Client()
        client.force_login(self.view_user)

        response = client.options(
            reverse(
                self.app_namespace + ':' + self.url_name + '-list',
                kwargs=self.url_kwargs
            ),
            content_type='application/json'
        )

        assert type(response.data['urls']['self']) is str
