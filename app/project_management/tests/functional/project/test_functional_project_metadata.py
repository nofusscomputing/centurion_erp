import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional, MetaDataNavigationEntriesFunctional

from project_management.models.projects import Project



@pytest.mark.module_project_management
class ViewSetBase(
    MetaDataNavigationEntriesFunctional,
    MetadataAttributesFunctional,
):

    model = Project

    app_namespace = 'v2'

    url_name = '_api_project'

    change_data = {'name': 'device-change'}

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

        self.global_org_item = self.model.objects.create(
            organization = self.global_organization,
            name = 'global_item'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one-add'
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two-add'
        )


        self.url_view_kwargs = {'pk': self.item.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }


        self.add_data_import_fields = {
            'name': 'team-post',
            'organization': self.organization.id,
            'external_ref': 1,
            'external_system': int(Project.Ticket_ExternalSystem.CUSTOM_1)
        }



@pytest.mark.model_project
class ProjectMetadata(
    ViewSetBase,
    TestCase
):

    menu_id = 'project_management'

    menu_entry_id = 'project'
