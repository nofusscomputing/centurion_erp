import django
import pytest

from django.test import TestCase

from access.models.tenant import Tenant as Organization

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

User = django.contrib.auth.get_user_model()



@pytest.mark.model_tenant
class ViewSetBase:

    model = Organization

    app_namespace = 'v2'
    
    url_name = '_api_tenant'

    change_data = {'name': 'device'}

    delete_data = {}

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


        self.add_data = {
            'name': 'team_post',
        }


        self.super_add_user = User.objects.create_user(username="test_user_add_super", password="password", is_superuser = True)

        super().setUpTestData()

        self.item = self.organization

        self.other_org_item = self.different_organization

        self.url_view_kwargs = { 'pk': self.item.id }



@pytest.mark.module_access
class OrganizationMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'access'

    menu_entry_id = 'tenant'