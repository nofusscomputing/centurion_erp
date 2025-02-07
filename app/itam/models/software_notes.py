from access.fields import *

from core.models.model_notes import ModelNotes

from itam.models.software import Software



class SoftwareNotes(
    ModelNotes
):


    class Meta:

        db_table = 'itam_software_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Software Note'

        verbose_name_plural = 'Software Notes'


    model = models.ForeignKey(
        Software,
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
