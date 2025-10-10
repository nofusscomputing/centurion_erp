import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from core.models.ticket_base import TicketBase



@pytest.mark.model_ticketbase
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

        self.presetUpTestData()

        self.kwargs_create_item.update({
            'opened_by': self.view_user,
            'organization': self.organization
        })

        self.kwargs_create_item_diff_org.update({
            'opened_by': self.view_user,
            'organization': self.different_organization
        })

        if self.model._meta.sub_model_type != 'ticket':
            self.url_view_kwargs.update({ 'ticket_type': self.model._meta.sub_model_type })

        super().setUpTestData()


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

    url_name = '_api_ticketbase_sub'


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
            'app_label': self.model._meta.app_label,
            'ticket_type': self.model._meta.sub_model_type
        }

        self.url_view_kwargs = {
            'app_label': self.model._meta.app_label,
            'ticket_type': self.model._meta.sub_model_type
        }

        super().setUpTestData()


@pytest.mark.module_core
class TicketBaseMetadataTest(
    MetadataTestCases,
    TestCase,

):

    url_name = '_api_ticketbase'


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


