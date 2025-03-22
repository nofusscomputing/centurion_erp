from django.db import models

from core.models.model_history import ModelHistory

from devops.models.git_group import GitGroup



class GitGroupHistory(
    ModelHistory
):


    class Meta:

        db_table = 'devops_git_group_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Git Group History'

        verbose_name_plural = 'Git Group History'


    model = models.ForeignKey(
        GitGroup,
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

        from devops.serializers.git_group import BaseSerializer

        model = BaseSerializer(self.model, context = serializer_context)

        return model
