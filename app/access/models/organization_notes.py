from django.db import models

from access.models.organization import Organization

from core.models.model_notes import ModelNotes



class OrganizationNotes(
    ModelNotes
):


    class Meta:

        db_table = 'access_organization_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Organization Note'

        verbose_name_plural = 'Organization Notes'


    model = models.ForeignKey(
        Organization,
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
