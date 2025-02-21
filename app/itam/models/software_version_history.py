from django.db import models

from core.models.model_history import ModelHistory

from itam.models.software import SoftwareVersion



class SoftwareVersionHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_softwareversion_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Software Version History'

        verbose_name_plural = 'Software Version History'


    model = models.ForeignKey(
        SoftwareVersion,
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

        from itam.serializers.software_version import SoftwareVersionBaseSerializer

        model = SoftwareVersionBaseSerializer(self.model, context = serializer_context)

        return model
