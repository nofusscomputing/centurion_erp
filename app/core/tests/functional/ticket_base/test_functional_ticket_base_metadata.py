import django

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models.tenant import Tenant as Organization
from access.models.team import Team
from access.models.team_user import TeamUsers

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from core.models.ticket_base import TicketBase

User = django.contrib.auth.get_user_model()



class MetadataTestCases(
    MetadataAttributesFunctional,
):

    add_data: dict = {
        'title': 'ticket one',
        'description': 'sadsa'
    }

    app_namespace = 'v2'

    base_model = TicketBase
    """Base model for this sub model
    don't change or override this value
    """

    change_data = None

    delete_data = {}

    kwargs_create_item: dict = {
        'title': 'ticket two',
        'description': 'sadsa'
    }

    kwargs_create_item_diff_org: dict = {
        'title': 'ticket three',
        'description': 'sadsa'
    }

    model = TicketBase

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

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

        self.view_user = User.objects.create_user(username="test_user_view", password="password")

        self.kwargs_create_item.update({
            'opened_by': self.view_user
        })

        self.item = self.model.objects.create(
            organization = organization,
            **self.kwargs_create_item
        )

        self.kwargs_create_item_diff_org.update({
            'opened_by': self.view_user
        })

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            **self.kwargs_create_item_diff_org
        )


        self.url_view_kwargs.update({ 'pk': self.item.id })

        if self.add_data is not None:

            self.add_data.update({
                'organization': self.organization.id,
                'opened_by': self.view_user
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


    def test_sanity_is_ticket_sub_model(self):
        """Sanity Test
        
        This test ensures that the model being tested `self.model` is a
        sub-model of `self.base_model`.
        This test is required as the same viewset is used for all sub-models
        of `TicketBase`
        """

        assert issubclass(self.model, self.base_model)



class TicketBaseMetadataInheritedCases(
    MetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    url_name = '_api_v2_ticket_sub'


    @classmethod
    def setUpTestData(self):

        self.kwargs_create_item = {
            **super().kwargs_create_item,
            **self.kwargs_create_item
        }

        self.kwargs_create_item_diff_org = {
            **super().kwargs_create_item_diff_org,
            **self.kwargs_create_item_diff_org
        }

        self.url_kwargs = {
            'ticket_model': self.model._meta.sub_model_type
        }

        self.url_view_kwargs = {
            'ticket_model': self.model._meta.sub_model_type
        }

        super().setUpTestData()



class TicketBaseMetadataTest(
    MetadataTestCases,
    TestCase,

):

    url_name = '_api_v2_ticket'


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


