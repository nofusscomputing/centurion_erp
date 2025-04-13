from django.test import TestCase

from access.models.organization import Organization

from app.tests.unit.test_unit_models import (
    TenancyObjectInheritedCases
)

from project_management.models.project_milestone import Project, ProjectMilestone


class ProjectMilestoneModel(
    TenancyObjectInheritedCases,
    TestCase,
):

    model = ProjectMilestone


    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Create an organization for user and item
        . create an organization that is different to item
        2. Create a device
        3. create teams with each permission: view, add, change, delete
        4. create a user per team
        """

        self.organization = Organization.objects.create(name='test_org')

        self.project = Project.objects.create(
            organization = self.organization,
            name = 'proj',
        )

        self.kwargs_item_create = {
            'name': 'mile',
            'project': self.project
        }

        super().setUpTestData()
