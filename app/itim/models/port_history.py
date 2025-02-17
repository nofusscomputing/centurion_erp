from django.db import models

from core.models.model_history import ModelHistory

from itim.models.services import Port



class PortHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itim_port_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Port History'

        verbose_name_plural = 'Port History'


    model = models.ForeignKey(
        Port,
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

        from itim.serializers.port import PortBaseSerializer

        model = PortBaseSerializer(self.model, context = serializer_context)

        return model
