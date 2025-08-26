import pytest

from django.test import TestCase

from access.models.role import Role

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional



@pytest.mark.model_role
class ViewSetBase:

    add_data: dict = None

    app_namespace = 'v2'

    change_data = { 'name': 'changed name' }

    delete_data = {}

    kwargs_create_item: dict = {}

    kwargs_create_item_diff_org: dict = {}

    kwargs_create_item_global_org_org: dict = {}

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

        super().presetUpTestData()

        self.kwargs_create_item['organization'] = self.organization
        self.kwargs_create_item['model_notes'] = 'some notes'


        self.kwargs_create_item_diff_org['organization'] = self.different_organization
        self.kwargs_create_item_diff_org['model_notes'] = 'some more notes'


        self.kwargs_create_item_global_org_org['organization'] = self.global_organization
        self.kwargs_create_item_global_org_org['model_notes'] = 'some more notes'

        self.global_org_item = self.model.objects.create(
            **self.kwargs_create_item_global_org_org
        )

        if self.add_data is not None:

            self.add_data.update({'organization': self.organization.id})

        super().setUpTestData()



@pytest.mark.module_access
class RoleMetadataTest(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase,

):

    kwargs_create_item: dict = { 'name': 'create item' }

    kwargs_create_item_diff_org: dict = { 'name': 'diff org create' }

    kwargs_create_item_global_org_org: dict = { 'name': 'global org create' }

    model = Role

    url_kwargs: dict = {}

    url_view_kwargs: dict = {}

    url_name = '_api_role'
