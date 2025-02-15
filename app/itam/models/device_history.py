from django.db import models

from core.models.model_history import ModelHistory

from itam.models.device import Device



class DeviceHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_device_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Device History'

        verbose_name_plural = 'Device History'


    model = models.ForeignKey(
        Device,
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

        from itam.serializers.device import DeviceBaseSerializer

        model = DeviceBaseSerializer(self.model, context = serializer_context)

        return model
