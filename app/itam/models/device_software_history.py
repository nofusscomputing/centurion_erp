from django.db import models

from itam.models.device import DeviceSoftware
from itam.models.device_history import (
    DeviceHistory
)



class DeviceSoftwareHistory(
    DeviceHistory
):


    class Meta:

        db_table = 'itam_devicesoftware_history'

        ordering = DeviceHistory._meta.ordering

        verbose_name = 'Device Software History'

        verbose_name_plural = 'Device Software History'


    child_model = models.ForeignKey(
        DeviceSoftware,
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

        from itam.serializers.software import SoftwareBaseSerializer

        model = SoftwareBaseSerializer(self.child_model.software, context = serializer_context)

        return model
