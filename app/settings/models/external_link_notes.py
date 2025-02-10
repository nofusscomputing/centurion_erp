from django.db import models

from core.models.model_notes import ModelNotes

from settings.models.external_link import ExternalLink



class ExternalLinkNotes(
    ModelNotes
):


    class Meta:

        db_table = 'settings_external_link_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'External Link Note'

        verbose_name_plural = 'External Link Notes'


    model = models.ForeignKey(
        ExternalLink,
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
