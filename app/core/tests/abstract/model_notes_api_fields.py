from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

from rest_framework.relations import Hyperlink

from access.models.organization import Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_fields import APITenancyObject



class ModelNotesNotesAPIFields(
    APITenancyObject
):
    """Base Model Notes Test Cases

    This Test Suite must be included in ALL model notes tests

    Args:
        APITenancyObject (class): Base test cases for ALL API fields
    """

    model = None

    view_name: str = None

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')

        self.view_user = User.objects.create_user(username="test_user_view", password="password", is_superuser = True)


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


    @classmethod
    def make_request(self):
        client = Client()
        url = reverse('v2:' + self.view_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



    def test_api_field_exists_model_notes(self):
        """ Test for existance of API Field

        This test case is to override a test case of the same name
        as this model does not have a `model_notes` field

        model_notes field must exist
        """

        pass


    def test_api_field_type_model_notes(self):
        """ Test for type for API Field

        This test case is to override a test case of the same name
        as this model does not have a `model_notes` field

        model_notes field must be str
        """

        pass









    def test_api_field_exists_content(self):
        """ Test for existance of API Field

        content field must exist
        """

        assert 'content' in self.api_data


    def test_api_field_type_content(self):
        """ Test for type for API Field

        content field must be str
        """

        assert type(self.api_data['content']) is str







    def test_api_field_exists_content_type(self):
        """ Test for existance of API Field

        content_type field must exist
        """

        assert 'content_type' in self.api_data


    def test_api_field_type_content_type(self):
        """ Test for type for API Field

        content_type field must be int
        """

        assert type(self.api_data['content_type']) is int










    def test_api_field_exists_created_by(self):
        """ Test for existance of API Field

        created_by field must exist
        """

        assert 'created_by' in self.api_data


    def test_api_field_type_created_by(self):
        """ Test for type for API Field

        created_by field must be dict
        """

        assert type(self.api_data['created_by']) is dict



    def test_api_field_exists_created_by_id(self):
        """ Test for existance of API Field

        created_by.id field must exist
        """

        assert 'id' in self.api_data['created_by']


    def test_api_field_type_created_by_id(self):
        """ Test for type for API Field

        created_by.id field must be int
        """

        assert type(self.api_data['created_by']['id']) is int


    def test_api_field_exists_created_by_display_name(self):
        """ Test for existance of API Field

        created_by.display_name field must exist
        """

        assert 'display_name' in self.api_data['created_by']


    def test_api_field_type_created_by_display_name(self):
        """ Test for type for API Field

        created_by.display_name field must be str
        """

        assert type(self.api_data['created_by']['display_name']) is str


    def test_api_field_exists_created_by_first_name(self):
        """ Test for existance of API Field

        created_by.first_name field must exist
        """

        assert 'first_name' in self.api_data['created_by']


    def test_api_field_type_created_by_first_name(self):
        """ Test for type for API Field

        created_by.first_name field must be str
        """

        assert type(self.api_data['created_by']['first_name']) is str


    def test_api_field_exists_created_by_last_name(self):
        """ Test for existance of API Field

        created_by.last_name field must exist
        """

        assert 'last_name' in self.api_data['created_by']


    def test_api_field_type_created_by_last_name(self):
        """ Test for type for API Field

        created_by.last_name field must be str
        """

        assert type(self.api_data['created_by']['last_name']) is str


    def test_api_field_exists_created_by_username(self):
        """ Test for existance of API Field

        created_by.username field must exist
        """

        assert 'username' in self.api_data['created_by']


    def test_api_field_type_created_by_username(self):
        """ Test for type for API Field

        created_by.username field must be str
        """

        assert type(self.api_data['created_by']['username']) is str


    def test_api_field_exists_created_by_is_active(self):
        """ Test for existance of API Field

        created_by.is_active field must exist
        """

        assert 'is_active' in self.api_data['created_by']


    def test_api_field_type_created_by_is_active(self):
        """ Test for type for API Field

        created_by.is_active field must be bool
        """

        assert type(self.api_data['created_by']['is_active']) is bool


    def test_api_field_exists_created_by_url(self):
        """ Test for existance of API Field

        created_by.url field must exist
        """

        assert 'url' in self.api_data['created_by']


    def test_api_field_type_created_by_url(self):
        """ Test for type for API Field

        created_by.url field must be Hyperlink
        """

        assert type(self.api_data['created_by']['url']) is Hyperlink





























    def test_api_field_exists_modified_by(self):
        """ Test for existance of API Field

        modified_by field must exist
        """

        assert 'modified_by' in self.api_data


    def test_api_field_type_modified_by(self):
        """ Test for type for API Field

        modified_by field must be dict
        """

        assert type(self.api_data['modified_by']) is dict



    def test_api_field_exists_modified_by_id(self):
        """ Test for existance of API Field

        modified_by.id field must exist
        """

        assert 'id' in self.api_data['modified_by']


    def test_api_field_type_modified_by_id(self):
        """ Test for type for API Field

        modified_by.id field must be int
        """

        assert type(self.api_data['modified_by']['id']) is int


    def test_api_field_exists_modified_by_display_name(self):
        """ Test for existance of API Field

        modified_by.display_name field must exist
        """

        assert 'display_name' in self.api_data['modified_by']


    def test_api_field_type_modified_by_display_name(self):
        """ Test for type for API Field

        modified_by.display_name field must be str
        """

        assert type(self.api_data['modified_by']['display_name']) is str


    def test_api_field_exists_modified_by_first_name(self):
        """ Test for existance of API Field

        modified_by.first_name field must exist
        """

        assert 'first_name' in self.api_data['modified_by']


    def test_api_field_type_modified_by_first_name(self):
        """ Test for type for API Field

        modified_by.first_name field must be str
        """

        assert type(self.api_data['modified_by']['first_name']) is str


    def test_api_field_exists_modified_by_last_name(self):
        """ Test for existance of API Field

        modified_by.last_name field must exist
        """

        assert 'last_name' in self.api_data['modified_by']


    def test_api_field_type_modified_by_last_name(self):
        """ Test for type for API Field

        modified_by.last_name field must be str
        """

        assert type(self.api_data['modified_by']['last_name']) is str


    def test_api_field_exists_modified_by_username(self):
        """ Test for existance of API Field

        modified_by.username field must exist
        """

        assert 'username' in self.api_data['modified_by']


    def test_api_field_type_modified_by_username(self):
        """ Test for type for API Field

        modified_by.username field must be str
        """

        assert type(self.api_data['modified_by']['username']) is str


    def test_api_field_exists_modified_by_is_active(self):
        """ Test for existance of API Field

        modified_by.is_active field must exist
        """

        assert 'is_active' in self.api_data['modified_by']


    def test_api_field_type_modified_by_is_active(self):
        """ Test for type for API Field

        modified_by.is_active field must be bool
        """

        assert type(self.api_data['modified_by']['is_active']) is bool


    def test_api_field_exists_modified_by_url(self):
        """ Test for existance of API Field

        modified_by.url field must exist
        """

        assert 'url' in self.api_data['modified_by']


    def test_api_field_type_modified_by_url(self):
        """ Test for type for API Field

        modified_by.url field must be Hyperlink
        """

        assert type(self.api_data['modified_by']['url']) is Hyperlink





