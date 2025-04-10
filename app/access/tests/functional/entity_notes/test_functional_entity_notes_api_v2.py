from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from access.models.entity_notes import Entity, EntityNotes

from core.tests.abstract.model_notes_api_fields import ModelNotesNotesAPIFields



class NotesAPITestCases(
    ModelNotesNotesAPIFields,
):

    entity_model = None

    model = EntityNotes

    kwargs_model_create: dict = None

    # url_view_kwargs: dict = None

    view_name: str = '_api_v2_entity_note'

    @classmethod
    def setUpTestData(self):
        """Setup Test

        1. Call parent setup
        2. Create a model note
        3. add url kwargs
        4. make the API request

        """

        super().setUpTestData()


        self.item = self.model.objects.create(
            organization = self.organization,
            content = 'a random comment',
            content_type = ContentType.objects.get(
                app_label = str(self.model._meta.app_label).lower(),
                model = str(self.model.model.field.related_model.__name__).replace(' ', '').lower(),
            ),
            model = self.entity_model.objects.create(
                organization = self.organization,
                model_notes = 'text',
                **self.kwargs_model_create
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )


        self.url_view_kwargs = {
            'model_id': self.item.model.pk,
            'pk': self.item.pk
            }

        self.make_request()



class EntityNotesAPIInheritedCases(
    NotesAPITestCases,
):

    entity_model = None

    kwargs_model_create = None



class EntityNotesAPITest(
    NotesAPITestCases,
    TestCase,
):

    entity_model = Entity

    kwargs_model_create = {}
