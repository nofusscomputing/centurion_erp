from django.db import models

from itam.models.device import DeviceOperatingSystem
from itam.models.device_history import (
    DeviceHistory
)



class DeviceOperatingSystemHistory(
    DeviceHistory
):


    class Meta:

        db_table = 'itam_deviceoperatingsystem_history'

        ordering = DeviceHistory._meta.ordering

        verbose_name = 'Device Operating System History'

        verbose_name_plural = 'Device Operating System History'


    child_model = models.ForeignKey(
        DeviceOperatingSystem,
        blank = False,
        help_text = 'Model this note belongs to',
        null = True,
        on_delete = models.SET_NULL,
        related_name = 'history',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_serialized_child_model(self, serializer_context):

        model = None

        from itam.serializers.operating_system import OperatingSystemBaseSerializer

        model = OperatingSystemBaseSerializer(self.child_model.operating_system_version.operating_system, context = serializer_context)

        return model
