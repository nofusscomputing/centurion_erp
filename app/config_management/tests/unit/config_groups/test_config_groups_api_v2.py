import django
import pytest
import unittest

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_fields import APITenancyObject

from config_management.models.groups import ConfigGroups

User = django.contrib.auth.get_user_model()



class ConfigGroupsAPI(
    TestCase,
    APITenancyObject
):

    model = ConfigGroups

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            config = dict({"key": "one", "existing": "dont_over_write"})
        )

        self.second_item = self.model.objects.create(
            organization = self.organization,
            name = 'one_two',
            model_notes = 'stuff',
            config = dict({"key": "two"}),
            parent = self.item
        )

        self.url_view_kwargs = {'pk': self.second_item.id}

        view_permissions = Permission.objects.get(
                codename = 'view_' + self.model._meta.model_name,
                content_type = ContentType.objects.get(
                    app_label = self.model._meta.app_label,
                    model = self.model._meta.model_name,
                )
            )

        view_team = Team.objects.create(
            team_name = 'view_team',
            organization = self.organization,
        )

        view_team.permissions.set([view_permissions])

        self.view_user = User.objects.create_user(username="test_user_view", password="password")
        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        client = Client()
        url = reverse('v2:_api_v2_config_group-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_config(self):
        """ Test for existance of API Field

        config field must exist
        """

        assert 'config' in self.api_data


    def test_api_field_type_config(self):
        """ Test for type for API Field

        config field must be dict
        """

        assert type(self.api_data['config']) is dict



    def test_api_field_exists_parent(self):
        """ Test for existance of API Field

        parent field must exist
        """

        assert 'parent' in self.api_data


    def test_api_field_type_parent(self):
        """ Test for type for API Field

        parent field must be dict
        """

        assert type(self.api_data['parent']) is dict


    def test_api_field_exists_parent_id(self):
        """ Test for existance of API Field

        parent.id field must exist
        """

        assert 'id' in self.api_data['parent']


    def test_api_field_type_parent_id(self):
        """ Test for type for API Field

        parent.id field must be int
        """

        assert type(self.api_data['parent']['id']) is int


    def test_api_field_exists_parent_display_name(self):
        """ Test for existance of API Field

        parent.display_name field must exist
        """

        assert 'display_name' in self.api_data['parent']


    def test_api_field_type_parent_display_name(self):
        """ Test for type for API Field

        parent.display_name field must be str
        """

        assert type(self.api_data['parent']['display_name']) is str


    def test_api_field_exists_parent_url(self):
        """ Test for existance of API Field

        parent.url field must exist
        """

        assert 'url' in self.api_data['parent']


    def test_api_field_type_parent_url(self):
        """ Test for type for API Field

        parent.url field must be str
        """

        assert type(self.api_data['parent']['url']) is str



    def test_api_field_exists_urls_tickets(self):
        """ Test for existance of API Field

        _urls.tickets field must exist
        """

        assert 'tickets' in self.api_data['_urls']


    def test_api_field_type_urls_tickets(self):
        """ Test for type for API Field

        _urls.tickets field must be str
        """

        assert type(self.api_data['_urls']['tickets']) is str
