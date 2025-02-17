from django.db import models

from core.models.model_history import ModelHistory

from settings.models.external_link import ExternalLink



class ExternalLinkHistory(
    ModelHistory
):


    class Meta:

        db_table = 'settings_externallink_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'External Link History'

        verbose_name_plural = 'External Link History'


    model = models.ForeignKey(
        ExternalLink,
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

        from settings.serializers.external_links import ExternalLinkBaseSerializer

        model = ExternalLinkBaseSerializer(self.model, context = serializer_context)

        return model
