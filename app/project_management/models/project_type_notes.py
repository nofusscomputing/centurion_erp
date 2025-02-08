from access.fields import *

from core.models.model_notes import ModelNotes

from project_management.models.project_types import ProjectType



class ProjectTypeNotes(
    ModelNotes
):


    class Meta:

        db_table = 'project_management_project_type_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Project Type Note'

        verbose_name_plural = 'Project Type Notes'


    model = models.ForeignKey(
        ProjectType,
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
