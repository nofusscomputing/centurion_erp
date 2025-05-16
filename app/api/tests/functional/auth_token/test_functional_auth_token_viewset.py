import django
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.models.tokens import AuthToken
from api.tests.abstract.api_permissions_viewset import (
    APIPermissionAdd,
    APIPermissionDelete,
    APIPermissionView,
)
from api.tests.abstract.api_serializer_viewset import (
    SerializerAdd,
    SerializerDelete,
    SerializerView,
)
from api.tests.abstract.test_metadata_functional import (
    MetadataAttributesFunctionalEndpoint,
    MetadataAttributesFunctionalBase,
)

User = django.contrib.auth.get_user_model()




class ViewSetBase:

    model = AuthToken

    app_namespace = 'v2'
    
    url_name = '_api_v2_user_settings_token'

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

        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        self.item = self.model.objects.create(
            note = 'a note',
            token = self.model().generate,
            user = self.view_user,
            expires = '2025-02-25T23:14Z'
        )

        self.item_delete = self.model.objects.create(
            note = 'a note',
            token = self.model().generate,
            user = self.delete_user,
            expires = '2025-02-25T23:14Z'
        )

        # self.item.default_organization = self.organization

        # self.item.save()


        self.url_view_kwargs = {
            'model_id': self.view_user.id,
            'pk': self.item.id,
        }

        self.url_kwargs = {
            'model_id': self.view_user.id,
        }

        self.add_data = {
            'note': 'a note',
            'token': self.model().generate,
            'expires': '2025-02-26T23:14Z'
        }



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



class PermissionsAPI(
    ViewSetBase,
    APIPermissionAdd,
    APIPermissionDelete,
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



    def test_add_has_permission(self):
        """ Check correct permission for add 

        Attempt to add as user with permission
        """

        url_kwargs = self.url_kwargs.copy()

        url_kwargs['model_id'] = self.add_user.id


        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.add_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 201


    def test_add_permission_view_denied(self):
        """ Check correct permission for add

        Attempt to add a user with view permission
        """

        url_kwargs = self.url_kwargs.copy()

        url_kwargs['model_id'] = self.add_user.id

        client = Client()
        if self.url_kwargs:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = url_kwargs)

        else:

            url = reverse(self.app_namespace + ':' + self.url_name + '-list')


        client.force_login(self.view_user)
        response = client.post(url, data=self.add_data)

        assert response.status_code == 403



    def test_delete_has_permission(self):
        """ Check correct permission for delete

        Delete item as user with delete permission
        """

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['model_id'] = self.delete_user.id
        url_view_kwargs['pk'] = self.item_delete.id

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=url_view_kwargs)


        client.force_login(self.delete_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 204


    def test_delete_permission_view_denied(self):
        """ Check correct permission for delete

        Attempt to delete as user with veiw permission only
        """

        url_view_kwargs = self.url_view_kwargs.copy()

        url_view_kwargs['model_id'] = self.delete_user.id
        url_view_kwargs['pk'] = self.item_delete.id

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_name + '-detail', kwargs=url_view_kwargs)


        client.force_login(self.view_user)
        response = client.delete(url, data=self.delete_data)

        assert response.status_code == 403



    def test_returned_results_only_user_orgs(self):
        """Test not required

        this test is not required as this model is not a tenancy model
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



class ViewSet(
    ViewSetBase,
    SerializerAdd,
    SerializerDelete,
    SerializerView,
    TestCase,
):

    pass



class Metadata(
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
