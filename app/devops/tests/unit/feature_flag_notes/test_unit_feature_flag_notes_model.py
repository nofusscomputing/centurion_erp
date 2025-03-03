from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_notes_model import ModelNotesModel

from devops.models.feature_flag_notes import FeatureFlagNotes

from itam.models.software import Software



class FeatureFlagNotesModel(
    ModelNotesModel,
    TestCase,
):

    model = FeatureFlagNotes


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
                name = 'one',
                software = Software.objects.create(
                    organization = self.organization,
                    name = 'soft',
                ),
                description = 'desc',
                model_notes = 'text',
                enabled = True
            ),
            created_by = self.user,
        )
