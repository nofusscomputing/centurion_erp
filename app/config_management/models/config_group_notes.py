from django.db import models

from core.models.model_notes import ModelNotes

from config_management.models.groups import ConfigGroups



class ConfigGroupNotes(
    ModelNotes
):


    class Meta:

        db_table = 'config_management_config_group_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Config Group Note'

        verbose_name_plural = 'Config Group Notes'


    model = models.ForeignKey(
        ConfigGroups,
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
