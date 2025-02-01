import pytest

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase
from django import urls

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions_viewset import (
    APIPermissionChange,
    APIPermissionView
)
from api.tests.abstract.api_serializer_viewset import (
    SerializerChange,
    SerializerView,
)
from api.tests.abstract.test_metadata_functional import (
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
)


from settings.models.user_settings import UserSettings



class ViewSetBase:

    model = UserSettings

    app_namespace = 'v2'
    
    url_name = '_api_v2_user_settings'

    change_data = {'device_model_is_global': True}

    delete_data = {}

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a team
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')

        self.different_organization = different_organization


        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = organization,
        )

        view_team.permissions.set([view_permissions])



        add_permissions = Permission.objects.get(
                codename = 'add_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        add_team = Team.objects.create(
            team_name = 'add_team',
            organization = organization,
        )

        add_team.permissions.set([add_permissions])



        change_permissions = Permission.objects.get(
                codename = 'change_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        change_team = Team.objects.create(
            team_name = 'change_team',
            organization = organization,
        )

        change_team.permissions.set([change_permissions])



        delete_permissions = Permission.objects.get(
                codename = 'delete_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        delete_team = Team.objects.create(
            team_name = 'delete_team',
            organization = organization,
        )

        delete_team.permissions.set([delete_permissions])


        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        self.item = self.model.objects.get( id = self.view_user.id )

        self.item.default_organization = self.organization

        self.item.save()


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }


        self.add_user = User.objects.create_user(username="test_user_add", password="password")
        teamuser = TeamUsers.objects.create(
            team = add_team,
            user = self.add_user
        )

        self.change_user = User.objects.create_user(username="test_user_change", password="password")
        teamuser = TeamUsers.objects.create(
            team = change_team,
            user = self.change_user
        )

        self.delete_user = User.objects.create_user(username="test_user_delete", password="password")
        teamuser = TeamUsers.objects.create(
            team = delete_team,
            user = self.delete_user
        )


        self.different_organization_user = User.objects.create_user(username="test_different_organization_user", password="password")


        different_organization_team = Team.objects.create(
            team_name = 'different_organization_team',
            organization = different_organization,
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



class UserSettingsPermissionsAPI(
    ViewSetBase,
    APIPermissionChange,
    APIPermissionView,
    TestCase,
):


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass



    def test_add_create_not_allowed(self):
        """ Check correct permission for add 

        Not allowed to add.
        Ensure that the list view for HTTP/POST does not exist.
        """

        with pytest.raises(urls.exceptions.NoReverseMatch) as e:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')

        assert e.typename == 'NoReverseMatch'



    def test_delete_has_permission(self):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 405



    def test_change_has_permission(self):
        """ Check correct permission for change

        Make change with user who has change permission
        """


        item = self.model.objects.get( id = self.change_user.id )

        item.default_organization = self.organization

        item.save()

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs={'pk': item.id})


        client.force_login(self.change_user)
        response = client.patch(url, data={'different_organization': self.different_organization.id}, content_type='application/json')

        assert response.status_code == 200


    def test_change_permission_view_denied(self):
        """ Ensure permission view cant make change

        This test case is a duplicate of a test case with the same name.
        As this is the users own settings, any permission a user has will grant
        them access as user settings do not use permissions

        Attempt to make change as user with view permission
        """

        pass


    def test_returned_results_only_user_orgs(self):
        """Test not required

        this test is not required as this model is not a tenancy model
        """

        pass


    def test_change_no_permission_denied(self):
        """ Ensure permission view cant make change

        This test case is a duplicate of a test case with the same name.
        This test is not required for this model as there are no permissions
        assosiated with accessing this model.

        Attempt to make change as user without permissions
        """

        pass


    def test_view_no_permission_denied(self):
        """ Check correct permission for view

        This test case is a duplicate of a test case with the same name.
        This test is not required for this model as there are no permissions
        assosiated with accessing this model.

        Attempt to view with user missing permission
        """

        pass





class UserSettingsViewSet(
    ViewSetBase,
    SerializerChange,
    SerializerView,
    TestCase,
):

    pass



class UserSettingsMetadata(
    ViewSetBase,
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
    TestCase
):

    viewset_type = 'detail'

    @classmethod
    def setUpTestData(self):

        super().setUpTestData()

        self.url_kwargs = self.url_view_kwargs
