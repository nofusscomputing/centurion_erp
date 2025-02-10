from access.fields import *

from core.models.model_notes import ModelNotes

from itam.models.operating_system import OperatingSystemVersion



class OperatingSystemVersionNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itam_operating_system_version_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Operating System Version Note'

        verbose_name_plural = 'Operating System Version Notes'


    model = models.ForeignKey(
        OperatingSystemVersion,
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
            'operating_system_id': self.model.operating_system.pk,
            'model_id': self.model.pk,
            'pk': self.pk
        }
