import pytest

from django.test import TestCase

from api.tests.abstract.test_metadata_functional import MetadataAttributesFunctional

from project_management.models.project_milestone import Project, ProjectMilestone



@pytest.mark.model_projectmilestone
class ViewSetBase(
    MetadataAttributesFunctional,
):

    model = ProjectMilestone

    app_namespace = 'v2'

    url_name = '_api_projectmilestone'

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

        project = Project.objects.create(
            organization = self.organization,
            name = 'proj milestone test'
        )

        project_b = Project.objects.create(
            organization = self.different_organization,
            name = 'proj b milestone test'
        )


        self.item = self.model.objects.create(
            organization = self.organization,
            name = 'one-add',
            project = project
        )

        self.other_org_item = self.model.objects.create(
            organization = self.different_organization,
            name = 'two-add',
            project = project_b
        )


        self.url_view_kwargs = {'project_id': project.id, 'pk': self.item.id}

        self.url_kwargs = {'project_id': project.id}

        self.add_data = {
            'name': 'team-post',
            'organization': self.organization.id,
        }



@pytest.mark.module_project_management
class ProjectMilestoneMetadata(
    ViewSetBase,
    TestCase
):

    pass
