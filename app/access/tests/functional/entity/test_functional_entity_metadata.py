import django
import pytest

from django.test import TestCase

from access.models.entity import Entity

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

User = django.contrib.auth.get_user_model()



class EntityMetadataTestCases(
    MetadataAttributesFunctional,
):

    add_data: dict = {}

    app_namespace = 'v2'

    base_model = Entity
    """Base model for this sub model
    don't change or override this value
    """

    change_data = None

    delete_data = {}

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    model = Entity

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

        super().presetUpTestData()

        self.kwargs_create_item.update({ 'organization': self.organization })


        self.kwargs_create_item_diff_org.update({ 'organization': self.different_organization })


        if self.add_data is not None:

            self.add_data.update({
                'organization': self.organization.id,
            })

        super().setUpTestData()


    def test_sanity_is_entity_sub_model(self):
        """Sanity Test
        
        This test ensures that the model being tested `self.model` is a
        sub-model of `self.base_model`.
        This test is required as the same viewset is used for all sub-models
        of `AssetBase`
        """

        assert issubclass(self.model, self.base_model)



class EntityMetadataInheritedCases(
    EntityMetadataTestCases,
):

    model = None

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    url_name = '_api_entity_sub'


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
            'model_name': self.model._meta.model_name
        }

        self.url_view_kwargs = {
            'model_name': self.model._meta.model_name
        }

        super().setUpTestData()



class EntityMetadataTest(
    EntityMetadataTestCases,
    TestCase,

):

    url_name = '_api_entity'


    def test_method_options_request_detail_data_key_layout_dicts_key_exists_name(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its a base model.')


    def test_method_options_request_detail_data_key_layout_dicts_key_exists_sections(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its a base model.')


    def test_method_options_request_detail_data_key_layout_dicts_key_type_name(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its a base model.')


    def test_method_options_request_detail_data_key_layout_dicts_key_type_sections(self):
        pytest.xfail( reason = 'Model not intended to be displayed in detail view as its a base model.')


    def test_method_options_request_detail_data_key_layout_is_list_of_dict(self):
        pytest.xfail(reason = 'Model not intended to be displayed in detail view as its a base model.')
