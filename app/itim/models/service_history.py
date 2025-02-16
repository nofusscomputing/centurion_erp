from django.db import models

from core.models.model_history import ModelHistory

from itim.models.services import Service



class ServiceHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itim_service_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Service History'

        verbose_name_plural = 'Service History'


    model = models.ForeignKey(
        Service,
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

        from itim.serializers.service import ServiceBaseSerializer

        model = ServiceBaseSerializer(self.model, context = serializer_context)

        return model
