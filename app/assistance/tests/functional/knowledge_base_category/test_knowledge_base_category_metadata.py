import pytest

from django.test import TestCase


from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from assistance.models.knowledge_base_category import KnowledgeBaseCategory



@pytest.mark.model_knowledgebasecategory
class ViewSetBase:

    model = KnowledgeBaseCategory

    app_namespace = 'v2'

    url_name = '_api_knowledgebasecategory'

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

        super().setUpTestData()


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one',
            target_user = self.view_user
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two',
            target_user = self.different_organization_user
        )


        self.url_view_kwargs = {'pk': self.item.id}



@pytest.mark.module_assistance
class KnowledgeBaseCategoryMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    TestCase
):

    pass
