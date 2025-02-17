from django.db import models

from core.models.model_history import ModelHistory

from config_management.models.config_groups_history import ConfigGroupsHistory
from config_management.models.groups import ConfigGroupSoftware



class ConfigGroupSoftwareHistory(
    ConfigGroupsHistory
):


    class Meta:

        db_table = 'config_management_configgroupsoftware_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Config Group Software History'

        verbose_name_plural = 'Config Groups Software History'


    child_model = models.ForeignKey(
        ConfigGroupSoftware,
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

        from itam.serializers.software import SoftwareBaseSerializer

        model = SoftwareBaseSerializer(self.child_model.software, context = serializer_context)

        return model
