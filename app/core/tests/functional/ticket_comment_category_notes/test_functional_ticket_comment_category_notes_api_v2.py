from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from core.tests.abstract.model_notes_api_fields import ModelNotesNotesAPIFields

from core.models.ticket.ticket_comment_category_notes import TicketCommentCategory, TicketCommentCategoryNotes



class NotesAPI(
    ModelNotesNotesAPIFields,
    TestCase,
):

    model = TicketCommentCategoryNotes

    view_name: str = '_api_v2_ticket_comment_category_note'

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
            model = TicketCommentCategory.objects.create(
                organization = self.organization,
                name = 'note model',
            ),
            created_by = self.view_user,
            modified_by = self.view_user,
        )


        self.url_view_kwargs = {
            'model_id': self.item.model.pk,
            'pk': self.item.pk
        }

        self.make_request()
