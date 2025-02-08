from access.fields import *

from core.models.model_notes import ModelNotes

from itam.models.software import SoftwareVersion



class SoftwareVersionNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itam_software_version_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Software Version Note'

        verbose_name_plural = 'Software Version Notes'


    model = models.ForeignKey(
        SoftwareVersion,
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
            'software_id': self.model.software.pk,
            'model_id': self.model.pk,
            'pk': self.pk
        }
