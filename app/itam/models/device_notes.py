from access.fields import *

from core.models.model_notes import ModelNotes

from itam.models.device import Device



class DeviceNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itam_device_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Device Note'

        verbose_name_plural = 'Device Notes'


    model = models.ForeignKey(
        Device,
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
