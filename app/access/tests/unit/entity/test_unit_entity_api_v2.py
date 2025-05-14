import django

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, TestCase

# from rest_framework.relations import Hyperlink

from access.models.entity import Entity
from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.api_fields import APITenancyObject

User = django.contrib.auth.get_user_model()



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

        if self.model._meta.model_name != 'entity':

            self.url_view_kwargs.update({
                'entity_model': self.item.entity_type,
            })

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



    def test_api_field_exists_entity_type(self):
        """ Test for existance of API Field

        entity_type field must exist
        """

        assert 'entity_type' in self.api_data


    def test_api_field_type_entity_type(self):
        """ Test for type for API Field

        entity_type field must be str
        """

        assert type(self.api_data['entity_type']) is str



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


    def test_api_field_type_url_history_value(self):
        """ Test for url value

        _urls.history field must use the endpoint for entity model
        """

        assert str(self.api_data['_urls']['history']).endswith('/' + str(self.item._meta.app_label) + '/' + str(self.item._meta.model_name) + '/' + str(self.item.pk) + '/history')



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

        _urls.knowledge_base field must use the endpoint for entity model
        """

        assert str(self.api_data['_urls']['knowledge_base']).endswith('/assistance/entity/' + str(self.item.pk) + '/knowledge_base')



class EntityAPIInheritedCases(
    APITestCases,
):

    kwargs_item_create: dict = None

    model = None

    url_ns_name = '_api_v2_entity_sub'


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create.update({
            'entity_type': self.model._meta.model_name
        })

        super().setUpTestData()


    def test_api_field_exists_entity_value(self):
        """ Test for value of API Field

        entity_type field must match model name
        """

        assert self.api_data['entity_type'] == self.model._meta.model_name



class EntityAPITest(
    APITestCases,
    TestCase,
):

    kwargs_item_create: dict = None

    model = Entity

    url_ns_name = '_api_v2_entity'


    @classmethod
    def setUpTestData(self):

        self.kwargs_item_create = {
            'entity_type': 'entity'
        }

        super().setUpTestData()