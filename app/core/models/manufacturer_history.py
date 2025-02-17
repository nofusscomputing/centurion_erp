from django.db import models

from core.models.model_history import ModelHistory

from core.models.manufacturer import Manufacturer



class ManufacturerHistory(
    ModelHistory
):


    class Meta:

        db_table = 'core_manufacturer_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Manufacturer History'

        verbose_name_plural = 'Manufacturer History'


    model = models.ForeignKey(
        Manufacturer,
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

        from core.serializers.manufacturer import ManufacturerBaseSerializer

        model = ManufacturerBaseSerializer(self.model, context = serializer_context)

        return model
