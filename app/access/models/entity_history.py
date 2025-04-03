from django.db import models

from access.models.entity import Entity

from core.models.model_history import ModelHistory

from devops.models.feature_flag import FeatureFlag



class EntityHistory(
    ModelHistory
):


    class Meta:

        db_table = 'access_entity_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Entity History'

        verbose_name_plural = 'Entity History'


    model = models.ForeignKey(
        Entity,
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

        from access.serializers.entity import BaseSerializer

        model = BaseSerializer(self.model, context = serializer_context)

        return model
