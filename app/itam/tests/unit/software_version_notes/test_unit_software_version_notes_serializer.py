from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_notes_serializer import ModelNotesSerializerTestCases

from itam.models.software import Software
from itam.serializers.software_version_notes import SoftwareVersionNotes, SoftwareVersionNoteModelSerializer



class SoftwareVersionNotesSerializer(
    ModelNotesSerializerTestCases,
    TestCase,
):

    model = SoftwareVersionNotes

    model_serializer = SoftwareVersionNoteModelSerializer


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        super().setUpTestData()


        self.software = Software.objects.create(
            organization = self.organization,
            name = 'os name',
        )
        self.note_model = self.model.model.field.related_model.objects.create(
            organization = self.organization,
            name = '11',
            software = self.software,
            
        )

        self.note_model_two = self.model.model.field.related_model.objects.create(
            organization = self.organization,
            name = '22',
            software = self.software,
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
                name = '33',
                software = self.software,
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
