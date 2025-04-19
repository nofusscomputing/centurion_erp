from django.test import TestCase

from access.models.organization import Organization

from core.tests.unit.model_notes.test_unit_model_notes_model import (
    ModelNotesInheritedCases
)

from project_management.models.projects import Project
from project_management.models.project_milestone_notes import ProjectMilestoneNotes



class ProjectMilestoneNotesModel(
    ModelNotesInheritedCases,
    TestCase,
):

    model = ProjectMilestoneNotes


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        self.organization = Organization.objects.create(name='test_org')

        self.kwargs_create_related_model: dict = {
            'organization': self.organization,
            'name': 'note model existing item',
            'project': Project.objects.create(
                organization = self.organization,
                name = 'note model existing item',
            )
        }

        super().setUpTestData()
