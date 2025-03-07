from django.db import models

from core.models.ticket.ticket_comment_category import TicketCommentCategory
from core.models.model_notes import ModelNotes



class TicketCommentCategoryNotes(
    ModelNotes
):


    class Meta:

        db_table = 'core_ticketcommentcategory_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Ticket Comment Category Note'

        verbose_name_plural = 'Ticket Comment Category Notes'


    model = models.ForeignKey(
        TicketCommentCategory,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'notes',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_url_kwargs(self) -> dict:

        return {
            'model_id': self.model.pk,
            'pk': self.pk
        }
