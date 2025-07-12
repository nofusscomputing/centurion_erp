import pytest
import django

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

# from rest_framework.relations import Hyperlink

from access.models.role import Role
from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_fields import APITenancyObject

User = django.contrib.auth.get_user_model()



@pytest.mark.model_role
class APITestCases(
    APITenancyObject,
):

    model = None

    kwargs_item_create: dict = None

    url_ns_name = None
    """Url namespace (optional, if not required) and url name"""


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        2. Create an item

        """

        self.organization = Organization.objects.create(name='test_org')


        self.item = self.model.objects.create(
            organization = self.organization,
            model_notes = 'random notes',
            **self.kwargs_item_create
        )


        self.url_view_kwargs = {
            'pk': self.item.id
        }

        # if self.model._meta.model_name != 'entity':

        #     self.url_view_kwargs.update({
        #         'model_name': self.item.entity_type,
        #     })


        # if self.model._meta.model_name != 'entity':

        #     self.url_view_kwargs.update({
        #         'entity_type': self.model._meta.model_name
        #     })

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
        url = reverse('v2:' + self.url_ns_name + '-detail', kwargs=self.url_view_kwargs)


        client.force_login(self.view_user)
        response = client.get(url)

        self.api_data = response.data



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


    # def test_api_field_type_url_history_value(self):
    #     """ Test for url value

    #     _urls.history field must use the endpoint for entity model
    #     """

    #     assert str(self.api_data['_urls']['history']).endswith('/access/role/' + str(self.item.pk) + '/history')



    def test_api_field_exists_url_knowledge_base(self):
        """ Test for existance of API Field

        _urls.knowledge_base field must exist
        """

        assert 'knowledge_base' in self.api_data['_urls']


    def test_api_field_type_url_knowledge_base(self):
        """ Test for type for API Field

        _urls.knowledge_base field must be str
        """

        assert type(self.api_data['_urls']['knowledge_base']) is str


    def test_api_field_type_url_knowledge_base_value(self):
        """ Test for url value

        _urls.knowledge_base field must use the endpoint for role model
        """

        assert str(self.api_data['_urls']['knowledge_base']).endswith('/assistance/role/' + str(self.item.pk) + '/knowledge_base')



@pytest.mark.module_role
class RoleAPITest(
    APITestCases,
    TestCase,
):

    kwargs_item_create: dict = None

    model = Role

    url_ns_name = '_api_v2_role'


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create = {
            'name': 'a role'
        }

        super().setUpTestData()