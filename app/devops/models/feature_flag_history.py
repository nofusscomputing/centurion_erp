from django.db import models

from core.models.model_history import ModelHistory

from devops.models.feature_flag import FeatureFlag



class FeatureFlagHistory(
    ModelHistory
):


    class Meta:

        db_table = 'devops_feature_flag_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Feature Flag History'

        verbose_name_plural = 'Feature Flags History'


    model = models.ForeignKey(
        FeatureFlag,
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

        from devops.serializers.feature_flag import BaseSerializer

        model = BaseSerializer(self.model, context = serializer_context)

        return model
