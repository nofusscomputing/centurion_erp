from django.db import models

from core.models.model_history import ModelHistory

from config_management.models.groups import ConfigGroups



class ConfigGroupsHistory(
    ModelHistory
):


    class Meta:

        db_table = 'config_management_configgroups_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Config Groups History'

        verbose_name_plural = 'Config Groups History'


    model = models.ForeignKey(
        ConfigGroups,
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

        from config_management.serializers.config_group import ConfigGroupBaseSerializer

        model = ConfigGroupBaseSerializer(self.model, context = serializer_context)

        return model
