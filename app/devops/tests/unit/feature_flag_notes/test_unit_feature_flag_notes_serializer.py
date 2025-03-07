from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_notes_serializer import ModelNotesSerializerTestCases

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag
from devops.serializers.feature_flag_notes import FeatureFlagNotes, FeatureFlagNoteModelSerializer

from itam.models.software import Software



class ManufacturerNotesSerializer(
    ModelNotesSerializerTestCases,
    TestCase,
):

    model = FeatureFlagNotes

    model_serializer = FeatureFlagNoteModelSerializer


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        super().setUpTestData()


        software = Software.objects.create(
            organization = self.organization,
            name = 'soft',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )


        self.note_model = self.model.model.field.related_model.objects.create(
            organization = self.organization,
            name = 'one',
            software = software,
            description = 'desc',
            model_notes = 'text',
            enabled = True
        )


        software = Software.objects.create(
            organization = self.organization,
            name = 'soft two',
        )

        SoftwareEnableFeatureFlag.objects.create(
            organization = self.organization,
            software = software,
            enabled = True
        )

        self.note_model_two = self.model.model.field.related_model.objects.create(
            organization = self.organization,
            name = 'two',
            software = software,
            description = 'desc',
            model_notes = 'text',
            enabled = True
        )


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
                software = software,
                description = 'desc',
                model_notes = 'text',
                enabled = True
            ),
            created_by = self.user_two,
        )


        self.valid_data = {
            'organization': self.organization_two.id,
            'content': 'a random comment',
            'content_type': self.content_type_two.id,
            'model': self.note_model_two.id,
            'created_by': self.user_two.id,
            'modified_by': self.user_two.id,
        }
