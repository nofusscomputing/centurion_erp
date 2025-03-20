from django.db import models

from core.models.model_history import ModelHistory

from devops.models.git_repository.github import GitHubRepository



class GitHubHistory(
    ModelHistory
):


    class Meta:

        db_table = 'devops_github_repository_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'GitHub Repository History'

        verbose_name_plural = 'GitHub Repository History'


    model = models.ForeignKey(
        GitHubRepository,
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

        from devops.serializers.git_repository.github import BaseSerializer

        model = BaseSerializer(self.model, context = serializer_context)

        return model
