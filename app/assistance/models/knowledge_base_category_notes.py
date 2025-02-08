from django.db import models

from core.models.model_notes import ModelNotes

from assistance.models.knowledge_base import KnowledgeBaseCategory



class KnowledgeCategoryBaseNotes(
    ModelNotes
):


    class Meta:

        db_table = 'assistance_knowledge_base_category_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Knowledge Base Category Note'

        verbose_name_plural = 'Knowledge Base Category Notes'


    model = models.ForeignKey(
        KnowledgeBaseCategory,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'notes',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_url_kwargs(self) -> dict:

        return {
            'model_id': self.model.pk,
            'pk': self.pk
        }
