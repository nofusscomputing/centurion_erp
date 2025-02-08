from access.fields import *

from core.models.model_notes import ModelNotes

from itim.models.services import Port



class PortNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itim_port_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Port Note'

        verbose_name_plural = 'Port Notes'


    model = models.ForeignKey(
        Port,
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
