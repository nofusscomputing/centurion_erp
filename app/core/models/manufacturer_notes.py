from django.db import models

from core.models.manufacturer import Manufacturer
from core.models.model_notes import ModelNotes



class ManufacturerNotes(
    ModelNotes
):


    class Meta:

        db_table = 'core_manufacturer_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Manufacturer Note'

        verbose_name_plural = 'Manufacturer Notes'


    model = models.ForeignKey(
        Manufacturer,
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
