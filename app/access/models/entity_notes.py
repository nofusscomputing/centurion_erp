from django.db import models

from access.models.entity import Entity

from core.models.model_notes import ModelNotes



class EntityNotes(
    ModelNotes
):


    class Meta:

        db_table = 'access_entity_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Entity Note'

        verbose_name_plural = 'Entity Notes'


    model = models.ForeignKey(
        Entity,
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
