from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models.organization import Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_fields import APITenancyObject

from devops.models.feature_flag import FeatureFlag

from itam.models.software import Software



class API(
    TestCase,
    APITenancyObject
):

    model = FeatureFlag

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
            software = Software.objects.create(
                organization = self.organization,
                name = 'soft',
            ),
            description = 'desc',
            model_notes = 'text',
            enabled = True
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
        TeamUsers.objects.create(
            team = view_team,
            user = self.view_user
        )

        client = Client()
        url = reverse('v2:devops:_api_v2_feature_flag-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_name(self):
        """ Test for existance of API Field

        name field must exist
        """

        assert 'name' in self.api_data


    def test_api_field_type_name(self):
        """ Test for type for API Field

        name field must be str
        """

        assert type(self.api_data['name']) is str



    def test_api_field_exists_url_history(self):
        """ Test for existance of API Field

        _urls.history field must exist
        """

        assert 'history' in self.api_data['_urls']


    def test_api_field_type_url_history(self):
        """ Test for type for API Field

        _urls.history field must be str
        """

        assert type(self.api_data['_urls']['history']) is str


    def test_api_field_exists_description(self):
        """ Test for existance of API Field

        description field must exist
        """

        assert 'description' in self.api_data


    def test_api_field_type_description(self):
        """ Test for type for API Field

        description field must be str
        """

        assert type(self.api_data['description']) is str


    def test_api_field_exists_enabled(self):
        """ Test for existance of API Field

        enabled field must exist
        """

        assert 'enabled' in self.api_data


    def test_api_field_type_enabled(self):
        """ Test for type for API Field

        enabled field must be bool
        """

        assert type(self.api_data['enabled']) is bool



    def test_api_field_exists_software(self):
        """ Test for existance of API Field

        software field must exist
        """

        assert 'software' in self.api_data


    def test_api_field_type_enabled(self):
        """ Test for type for API Field

        software field must be dict
        """

        assert type(self.api_data['software']) is dict


    def test_api_field_exists_software_id(self):
        """ Test for existance of API Field

        software.id field must exist
        """

        assert 'id' in self.api_data['software']


    def test_api_field_type_software_id(self):
        """ Test for type for API Field

        software.id field must be int
        """

        assert type(self.api_data['software']['id']) is int


    def test_api_field_exists_software_display_name(self):
        """ Test for existance of API Field

        software.display_name field must exist
        """

        assert 'display_name' in self.api_data['software']


    def test_api_field_type_software_display_name(self):
        """ Test for type for API Field

        software.display_name field must be str
        """

        assert type(self.api_data['software']['display_name']) is str


    def test_api_field_exists_software_url(self):
        """ Test for existance of API Field

        software.url field must exist
        """

        assert 'url' in self.api_data['software']


    def test_api_field_type_software_url(self):
        """ Test for type for API Field

        software.url field must be Hyperlink
        """

        assert type(self.api_data['software']['url']) is Hyperlink
