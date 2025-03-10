from django.db import models

from core.models.ticket.ticket_category import TicketCategory
from core.models.model_notes import ModelNotes



class TicketCategoryNotes(
    ModelNotes
):


    class Meta:

        db_table = 'core_ticketcategory_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Ticket Category Note'

        verbose_name_plural = 'Ticket Category Notes'


    model = models.ForeignKey(
        TicketCategory,
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
