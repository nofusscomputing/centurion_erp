from django.db import models

from core.models.model_history import ModelHistory

from access.models.organization import Organization



class OrganizationHistory(
    ModelHistory
):


    class Meta:

        db_table = 'access_organization_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Organization History'

        verbose_name_plural = 'Organization History'


    model = models.ForeignKey(
        Organization,
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

        from access.serializers.organization import OrganizationBaseSerializer

        model = OrganizationBaseSerializer(self.model, context = serializer_context)

        return model
