import django
import pytest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models.role import Role
from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional
from api.tests.abstract.api_permissions_viewset import APIPermissions
from api.tests.abstract.api_serializer_viewset import SerializersTestCases

from settings.models.app_settings import AppSettings

User = django.contrib.auth.get_user_model()



@pytest.mark.model_role
@pytest.mark.model_role
class ViewSetBase:

    add_data: dict = None

    app_namespace = 'v2'

    change_data = { 'name': 'changed name' }

    delete_data = {}

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    kwargs_create_item_global_org_org: dict = {}

    model = None

    url_kwargs: dict = None

    url_view_kwargs: dict = None

    url_name = None


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

        self.different_organization = Organization.objects.create(name='test_different_organization')

        self.global_organization = Organization.objects.create(name='test_global_organization')

        app_settings = AppSettings.objects.get(
            owner_organization = None
        )

        app_settings.global_organization = self.global_organization

        app_settings.save()


        self.item = self.model.objects.create(
            organization = organization,
            model_notes = 'some notes',
            **self.kwargs_create_item
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            model_notes = 'some more notes',
            **self.kwargs_create_item_diff_org
        )

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            model_notes = 'some more notes',
            **self.kwargs_create_item_global_org_org
        )


        # self.url_kwargs = {'organization_id': self.organization.id}

        self.url_view_kwargs.update({ 'pk': self.item.id })

        if self.add_data is not None:

            self.add_data.update({'organization': self.organization.id})


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
        TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

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



class RolePermissionsAPITest(
    ViewSetBase,
    APIPermissions,
    TestCase,
):

    add_data: dict = { 'name': 'added model note' }

    kwargs_create_item: dict = { 'name': 'create item' }

    kwargs_create_item_diff_org: dict = { 'name': 'diff org create' }

    kwargs_create_item_global_org_org: dict = { 'name': 'global org create' }

    model = Role

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_role'



class RoleViewSetTest(
    ViewSetBase,
    SerializersTestCases,
    TestCase,
):

    kwargs_create_item: dict = { 'name': 'create item' }

    kwargs_create_item_diff_org: dict = { 'name': 'diff org create' }

    kwargs_create_item_global_org_org: dict = { 'name': 'global org create' }

    model = Role

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_role'



class RoleMetadataTest(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase,

):

    kwargs_create_item: dict = { 'name': 'create item' }

    kwargs_create_item_diff_org: dict = { 'name': 'diff org create' }

    kwargs_create_item_global_org_org: dict = { 'name': 'global org create' }

    model = Role

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_role'
