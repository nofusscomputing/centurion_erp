from django.db import models

from core.models.model_history import ModelHistory

from itam.models.software import SoftwareCategory



class SoftwareCategoryHistory(
    ModelHistory
):


    class Meta:

        db_table = 'itam_softwarecategory_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Software Category History'

        verbose_name_plural = 'Software Category History'


    model = models.ForeignKey(
        SoftwareCategory,
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

        from itam.serializers.software_category import SoftwareCategoryBaseSerializer

        model = SoftwareCategoryBaseSerializer(self.model, context = serializer_context)

        return model
