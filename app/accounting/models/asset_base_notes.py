from django.db import models

from accounting.models.asset_base import AssetBase

from core.models.model_notes import ModelNotes



class AssetBaseNotes(
    ModelNotes
):


    class Meta:

        db_table = 'accounting_assetbase_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Asset Note'

        verbose_name_plural = 'Asset Notes'


    model = models.ForeignKey(
        AssetBase,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'notes',
        verbose_name = 'Model',
    )

    app_namespace = 'accounting'

    table_fields: list = []

    page_layout: dict = []


    def get_url_kwargs(self) -> dict:

        return {
            'model_id': self.model.pk,
            'pk': self.pk
        }
