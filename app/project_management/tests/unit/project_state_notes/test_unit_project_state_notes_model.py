from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_notes_model import ModelNotesModel

from project_management.models.project_state_notes import ProjectStateNotes



class ProjectStateNotesModel(
    ModelNotesModel,
    TestCase,
):

    model = ProjectStateNotes


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        super().setUpTestData()


        self.item = self.model.objects.create(
            organization = self.organization,
            content = 'a random comment for an exiting item',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = self.model.model.field.related_model.objects.create(
                organization = self.organization,
                name = 'note model existing item',
            ),
            created_by = self.user,
        )
