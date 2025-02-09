from django.db import models

from core.models.model_notes import ModelNotes

from itam.models.device import DeviceType



class DeviceTypeNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itam_device_type_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Device Type Note'

        verbose_name_plural = 'Device TypeNotes'


    model = models.ForeignKey(
        DeviceType,
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
