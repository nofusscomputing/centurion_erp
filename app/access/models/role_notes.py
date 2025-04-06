from django.db import models

from access.models.role import Role

from core.models.model_notes import ModelNotes



class RoleNotes(
    ModelNotes
):


    class Meta:

        db_table = 'access_role_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Role Note'

        verbose_name_plural = 'Role Notes'


    model = models.ForeignKey(
        Role,
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
