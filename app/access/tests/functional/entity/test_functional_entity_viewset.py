from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import Client, TestCase

from rest_framework.reverse import reverse

from access.models.entity import Entity
from access.models.organization import Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional
from api.tests.abstract.api_permissions_viewset import APIPermissions
from api.tests.abstract.api_serializer_viewset import SerializersTestCases



class ViewSetBase:

    add_data: dict = None

    app_namespace = 'v2'

    change_data = None

    delete_data = {}

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

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


        # self.url_kwargs = {'organization_id': self.organization.id}

        self.url_view_kwargs.update({ 'pk': self.item.id })

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



class PermissionsAPITestCases(
    ViewSetBase,
    APIPermissions,
):

    add_data: dict = { 'model_note': 'added model note' }

    change_data = {'model_notes': 'device'}

    model = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    url_kwargs: dict = None

    url_view_kwargs: dict = None

    url_name = None


    def test_returned_data_from_user_and_global_organizations_only(self):
        """Check items returned

        This test case is a over-ride of a test case with the same name.
        This model is not a tenancy model making this test not-applicable.

        Items returned from the query Must be from the users organization and
        global ONLY!
        """
        pass



class PermissionsAPIInheritedCases(
    PermissionsAPITestCases,
):

    add_data: dict = None

    model = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    url_name = '_api_v2_entity_sub'


    @classmethod
    def setUpTestData(self):

        self.url_kwargs = {
            'entity_model': self.model._meta.model_name
        }

        self.url_view_kwargs = {
            'entity_model': self.model._meta.model_name
        }

        super().setUpTestData()



class TeamPermissionsAPITest(
    PermissionsAPITestCases,
    TestCase,
):

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    model = Entity

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_v2_entity'




class ViewSetTestCases(
    ViewSetBase,
    SerializersTestCases,
):

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    model = None

    url_kwargs: dict = None

    url_view_kwargs: dict = None

    url_name = None



class ViewSetInheritedCases(
    ViewSetTestCases,
):

    model = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    url_name = '_api_v2_entity_sub'


    @classmethod
    def setUpTestData(self):

        self.url_kwargs = {
            'entity_model': self.model._meta.model_name
        }

        self.url_view_kwargs = {
            'entity_model': self.model._meta.model_name
        }

        super().setUpTestData()



class TeamViewSetTest(
    ViewSetTestCases,
    TestCase,
):

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    model = Entity

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_v2_entity'



class MetadataTestCases(
    ViewSetBase,
    MetadataAttributesFunctional,
):

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    model = None

    url_kwargs: dict = None

    url_view_kwargs: dict = None

    url_name = None



class MetadataInheritedCases(
    MetadataTestCases,
):

    model = None

    kwargs_create_item: dict = None

    kwargs_create_item_diff_org: dict = None

    url_name = '_api_v2_entity_sub'


    @classmethod
    def setUpTestData(self):

        self.url_kwargs = {
            'entity_model': self.model._meta.model_name
        }

        self.url_view_kwargs = {
            'entity_model': self.model._meta.model_name
        }

        super().setUpTestData()



class TeamMetadataTest(
    MetadataTestCases,
    TestCase,

):

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    model = Entity

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_v2_entity'


    # def test_method_options_request_detail_data_has_key_urls_back(self):
    #     """Test HTTP/Options Method

    #     Ensure the request data returned has key `urls.back`
    #     """

    #     client = Client()
    #     client.force_login(self.view_user)

    #     response = client.options(
    #         reverse(
    #             self.app_namespace + ':' + self.url_name + '-detail',
    #             kwargs=self.url_view_kwargs
    #         ),
    #         content_type='application/json'
    #     )

    #     assert 'back' in response.data['urls']


    # def test_method_options_request_detail_data_key_urls_back_is_str(self):
    #     """Test HTTP/Options Method

    #     Ensure the request data key `urls.back` is str
    #     """

    #     client = Client()
    #     client.force_login(self.view_user)

    #     response = client.options(
    #         reverse(
    #             self.app_namespace + ':' + self.url_name + '-detail',
    #             kwargs=self.url_view_kwargs
    #         ),
    #         content_type='application/json'
    #     )

    #     assert type(response.data['urls']['back']) is str



    # def test_method_options_request_list_data_has_key_urls_return_url(self):
    #     """Test HTTP/Options Method

    #     Ensure the request data returned has key `urls.return_url`
    #     """

    #     client = Client()
    #     client.force_login(self.view_user)

    #     if self.url_kwargs:

    #         url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

    #     else:

    #         url = reverse(self.app_namespace + ':' + self.url_name + '-list')

    #     response = client.options( url, content_type='application/json' )

    #     assert 'return_url' in response.data['urls']


    # def test_method_options_request_list_data_key_urls_return_url_is_str(self):
    #     """Test HTTP/Options Method

    #     Ensure the request data key `urls.return_url` is str
    #     """

    #     client = Client()
    #     client.force_login(self.view_user)

    #     if self.url_kwargs:

    #         url = reverse(self.app_namespace + ':' + self.url_name + '-list', kwargs = self.url_kwargs)

    #     else:

    #         url = reverse(self.app_namespace + ':' + self.url_name + '-list')

    #     response = client.options( url, content_type='application/json' )

    #     assert type(response.data['urls']['return_url']) is str


