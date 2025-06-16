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

from api.models.tokens import AuthToken
from api.tests.abstract.api_fields import APIModelFields

from core.models.manufacturer import Manufacturer

User = django.contrib.auth.get_user_model()



class API(
    TestCase,
    APIModelFields
):

    model = AuthToken

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.view_user = User.objects.create_user(username="test_user_view", password="password")

        self.item = self.model.objects.create(
            note = 'a note',
            token = self.model().generate,
            user = self.view_user,
            expires = '2099-02-26T00:53Z'
        )

        self.url_view_kwargs = {
            'model_id': self.view_user.id,
            'pk': self.item.id
        }

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

        teamuser = TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        client = Client()
        url = reverse('v2:_api_usersettings_token-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        This test case is a duplicate of a test with the same name. This
        model is not a tenancy model and does not require this field.

        model_notes field must exist
        """

        assert 'model_notes' not in self.api_data


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        This test case is a duplicate of a test with the same name. This
        model is not a tenancy model and does not require this field.

        model_notes field must be str
        """

        assert 'model_notes' not in self.api_data



    def test_api_field_exists_user(self):
        """ Test for existance of API Field

        user field must exist
        """

        assert 'user' in self.api_data


    def test_api_field_type_user(self):
        """ Test for type for API Field

        normallay an object would be serialized. However in this case only
        the owner of the object will access the object and therefore would
        be a waste to serialize it.

        user field must be int
        """

        assert type(self.api_data['user']) is int



    def test_api_field_exists_note(self):
        """ Test for existance of API Field

        note field must exist
        """

        assert 'note' in self.api_data


    def test_api_field_type_user(self):
        """ Test for type for API Field

        note field must be str
        """

        assert type(self.api_data['note']) is str



    def test_api_field_exists_expires(self):
        """ Test for existance of API Field

        expires field must exist
        """

        assert 'expires' in self.api_data


    def test_api_field_type_expires(self):
        """ Test for type for API Field

        expires field must be str
        """

        assert type(self.api_data['expires']) is str



    # def test_api_field_exists_url_history(self):
    #     """ Test for existance of API Field

    #     _urls.history field must exist
    #     """

    #     assert 'history' in self.api_data['_urls']


    # def test_api_field_type_url_history(self):
    #     """ Test for type for API Field

    #     _urls.history field must be str
    #     """

    #     assert type(self.api_data['_urls']['history']) is str
