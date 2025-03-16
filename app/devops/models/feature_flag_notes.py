from django.db import models

from core.models.model_notes import ModelNotes

from devops.models.feature_flag import FeatureFlag



class FeatureFlagNotes(
    ModelNotes
):


    class Meta:

        db_table = 'devops_feature_flag_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Feature Flag Note'

        verbose_name_plural = 'Feature Flag Notes'


    model = models.ForeignKey(
        FeatureFlag,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'notes',
        verbose_name = 'Model',
    )

    app_namespace = 'devops'

    table_fields: list = []

    page_layout: dict = []


    def get_url_kwargs(self) -> dict:

        return {
            'model_id': self.model.pk,
            'pk': self.pk
        }
