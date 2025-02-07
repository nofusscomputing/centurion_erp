from access.fields import *

from core.models.model_notes import ModelNotes

from itam.models.operating_system import OperatingSystem



class OperatingSystemNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itam_operating_system_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Operating System Note'

        verbose_name_plural = 'Operating System Notes'


    model = models.ForeignKey(
        OperatingSystem,
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
