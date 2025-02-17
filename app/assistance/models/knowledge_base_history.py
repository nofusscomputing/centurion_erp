from django.db import models

from core.models.model_history import ModelHistory

from assistance.models.knowledge_base import KnowledgeBase



class KnowledgeBaseHistory(
    ModelHistory
):


    class Meta:

        db_table = 'assistance_knowledge_base_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Knowledge Base History'

        verbose_name_plural = 'Knowledge Base History'


    model = models.ForeignKey(
        KnowledgeBase,
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

        from assistance.serializers.knowledge_base import KnowledgeBaseBaseSerializer

        model = KnowledgeBaseBaseSerializer(self.model, context = serializer_context)

        return model
