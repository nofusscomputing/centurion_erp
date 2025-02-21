from django.db import models

from core.models.model_history import ModelHistory

from itam.models.software import Software



class SoftwareHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_software_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Software History'

        verbose_name_plural = 'Software History'


    model = models.ForeignKey(
        Software,
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

        from itam.serializers.software import SoftwareBaseSerializer

        model = SoftwareBaseSerializer(self.model, context = serializer_context)

        return model
