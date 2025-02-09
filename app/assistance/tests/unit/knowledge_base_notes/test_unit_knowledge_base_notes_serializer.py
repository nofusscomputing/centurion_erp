from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.test_unit_model_notes_serializer import ModelNotesSerializerTestCases

from assistance.serializers.knowledge_base_notes import KnowledgeBaseNotes, KnowledgeBaseNoteModelSerializer



class KnowledgeBaseNotesSerializer(
    ModelNotesSerializerTestCases,
    TestCase,
):

    model = KnowledgeBaseNotes

    model_serializer = KnowledgeBaseNoteModelSerializer


    @classmethod
    def setUpTestData(self):
        """Setup Test"""

        super().setUpTestData()


        self.note_model = self.model.model.field.related_model.objects.create(
            organization = self.organization,
            title = 'note model',
            content = 'data',
        )

        self.note_model_two = self.model.model.field.related_model.objects.create(
            organization = self.organization,
            title = 'note model two',
            content = 'data',
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
                title = 'note model existing item',
                content = 'data',
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
