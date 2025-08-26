import pytest

from django.test import TestCase


from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from assistance.models.knowledge_base import KnowledgeBase, KnowledgeBaseCategory



@pytest.mark.model_knowledgebase
class ViewSetBase:

    model = KnowledgeBase

    app_namespace = 'v2'
    
    url_name = '_api_knowledgebase'

    change_data = {'title': 'device'}

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

        self.url_kwargs = {}

        super().setUpTestData()

        category_item = KnowledgeBaseCategory.objects.create(
            organization = self.organization,
            name = 'cat'
        )

        self.item = self.model.objects.create(
            organization = self.organization,
            title = 'one',
            content = 'some text for body',
            target_user = self.view_user,
            category = category_item,
        )

        category = KnowledgeBaseCategory.objects.create(
            organization = self.different_organization,
            name = 'cat1'
        )
        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            title = 'two',
            content = 'some text for body',
            target_user = self.different_organization_user,
            category = category,
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'title': 'team_post',
            'organization': self.organization.id,
            'content': 'article text',
            'target_user': self.view_user.id,
            'category': category_item.id,
        }


@pytest.mark.module_assistance
class KnowledgeBaseMetadata(
    ViewSetBase,
    MetadataAttributesFunctional,
    MetaDataNavigationEntriesFunctional,
    TestCase
):

    menu_id = 'assistance'

    menu_entry_id = 'knowledge_base'
