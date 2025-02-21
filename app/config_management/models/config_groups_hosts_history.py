from django.db import models

from core.models.model_history import ModelHistory

from config_management.models.config_groups_history import ConfigGroupsHistory
from config_management.models.groups import ConfigGroupHosts



class ConfigGroupHostsHistory(
    ConfigGroupsHistory
):


    class Meta:

        db_table = 'config_management_configgrouphosts_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Config Group Hosts History'

        verbose_name_plural = 'Config Groups Hosts History'


    child_model = models.ForeignKey(
        ConfigGroupHosts,
        blank = False,
        help_text = 'Model this note belongs to',
        null = True,
        on_delete = models.SET_NULL,
        related_name = 'history',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_object(self):

        return self


    def get_serialized_child_model(self, serializer_context):

        model = None

        from itam.serializers.device import DeviceBaseSerializer

        model = DeviceBaseSerializer(self.child_model.host, context = serializer_context)
        return model
