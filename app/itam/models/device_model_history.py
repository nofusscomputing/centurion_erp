from django.db import models

from core.models.model_history import ModelHistory

from itam.models.device_models import DeviceModel



class DeviceModelHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_devicemodel_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Device Model History'

        verbose_name_plural = 'Device Model History'


    model = models.ForeignKey(
        DeviceModel,
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

        from itam.serializers.device_model import DeviceModelBaseSerializer

        model = DeviceModelBaseSerializer(self.model, context = serializer_context)

        return model
