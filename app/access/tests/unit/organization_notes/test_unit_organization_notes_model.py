from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_notes_model import ModelNotesModel

from access.models.organization_notes import OrganizationNotes



class OrganizationNotesModel(
    ModelNotesModel,
    TestCase,
):

    model = OrganizationNotes


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
                name = 'note model existing item',
            ),
            created_by = self.user,
        )
