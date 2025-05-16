from django.db import models

from accounting.models.asset_base import AssetBase

from core.models.model_history import ModelHistory



class AssetBaseHistory(
    ModelHistory
):


    class Meta:

        db_table = 'accounting_assetbase_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Asset History'

        verbose_name_plural = 'Asset History'


    model = models.ForeignKey(
        AssetBase,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'history',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_object(self):

        return self


    def get_serialized_model(self, serializer_context):

        model = None

        from accounting.serializers.asset import BaseSerializer

        model = BaseSerializer(self.model, context = serializer_context)

        return model
