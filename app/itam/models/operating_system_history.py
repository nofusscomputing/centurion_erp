from django.db import models

from core.models.model_history import ModelHistory

from itam.models.operating_system import OperatingSystem



class OperatingSystemHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_operatingsystem_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Operating System History'

        verbose_name_plural = 'Operating System History'


    model = models.ForeignKey(
        OperatingSystem,
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

        from itam.serializers.operating_system import OperatingSystemBaseSerializer

        model = OperatingSystemBaseSerializer(self.model, context = serializer_context)

        return model
