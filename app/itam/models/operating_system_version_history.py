from django.db import models

from core.models.model_history import ModelHistory

from itam.models.operating_system import OperatingSystemVersion



class OperatingSystemVersionHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_operatingsystemversion_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Operating System Version History'

        verbose_name_plural = 'Operating Version System History'


    model = models.ForeignKey(
        OperatingSystemVersion,
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

        from itam.serializers.operating_system_version import OperatingSystemVersionBaseSerializer

        model = OperatingSystemVersionBaseSerializer(self.model, context = serializer_context)

        return model
