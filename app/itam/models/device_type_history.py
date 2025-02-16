from django.db import models

from core.models.model_history import ModelHistory

from itam.models.device import DeviceType



class DeviceTypeHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_devicetype_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Device Type History'

        verbose_name_plural = 'Device TYpe History'


    model = models.ForeignKey(
        DeviceType,
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

        from itam.serializers.device_type import DeviceTypeBaseSerializer

        model = DeviceTypeBaseSerializer(self.model, context = serializer_context)

        return model
