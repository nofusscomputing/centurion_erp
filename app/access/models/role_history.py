from django.db import models

from core.models.model_history import ModelHistory

from access.models.role import Role



class RoleHistory(
    ModelHistory
):


    class Meta:

        db_table = 'access_role_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Role History'

        verbose_name_plural = 'Role History'


    model = models.ForeignKey(
        Role,
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

        from access.serializers.role import BaseSerializer

        model = BaseSerializer(self.model, context = serializer_context)

        return model
