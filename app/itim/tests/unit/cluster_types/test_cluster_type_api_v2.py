import pytest
import unittest

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_fields import APITenancyObject

from itim.models.clusters import ClusterType



class ClusterTypeAPI(
    TestCase,
    APITenancyObject
):

    model = ClusterType

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
            config = dict({"one": "two"}),
            model_notes = 'a note'
        )

        self.url_view_kwargs = {'pk': self.item.id}

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
        url = reverse('v2:_api_v2_cluster_type-detail', kwargs=self.url_view_kwargs)


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

