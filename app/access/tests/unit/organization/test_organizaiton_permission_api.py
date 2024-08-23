import pytest
import unittest

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models import Organization, Team, TeamUsers, Permission

from api.tests.abstract.api_permissions import APIPermissionChange, APIPermissionView



class OrganizationPermissionsAPI(TestCase, APIPermissionChange, APIPermissionView):

    model = Organization

    model_name = 'organization'
    app_label = 'access'

    app_namespace = 'API'
    
    url_name = '_api_organization'

    url_list = '_api_orgs'

    change_data = {'name': 'device'}

    # delete_data = {'device': 'device'}

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        organization = Organization.objects.create(name='test_org')

        self.organization = organization

        different_organization = Organization.objects.create(name='test_different_organization')


        self.item = organization

        self.url_view_kwargs = {'pk': self.item.id}

        self.url_kwargs = {'pk': self.item.id}

        # self.add_data = {'name': 'device', 'organization': self.organization.id}


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


        self.super_user = User.objects.create_user(username="super_user", password="password", is_superuser=True)

        self.no_permissions_user = User.objects.create_user(username="test_no_permissions", password="password")


        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

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


    def test_add_is_prohibited_anon_user(self):
        """ Ensure Organization cant be created 

        Attempt to create organization as anon user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_list)


        # client.force_login(self.add_user)
        response = client.post(url, data={'name': 'should not create'}, content_type='application/json')

        assert response.status_code == 401


    def test_add_is_prohibited_diff_org_user(self):
        """ Ensure Organization cant be created 

        Attempt to create organization as user with different org permissions.
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_list)


        client.force_login(self.different_organization_user)
        response = client.post(url, data={'name': 'should not create'}, content_type='application/json')

        assert response.status_code == 405


    def test_add_is_prohibited_super_user(self):
        """ Ensure Organization cant be created 

        Attempt to create organization as user who is super user
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_list)


        client.force_login(self.super_user)
        response = client.post(url, data={'name': 'should not create'}, content_type='application/json')

        assert response.status_code == 405


    def test_add_is_prohibited_user_same_org(self):
        """ Ensure Organization cant be created 

        Attempt to create organization as user with permission
        """

        client = Client()
        url = reverse(self.app_namespace + ':' + self.url_list)


        client.force_login(self.add_user)
        response = client.post(url, data={'name': 'should not create'}, content_type='application/json')

        assert response.status_code == 405
