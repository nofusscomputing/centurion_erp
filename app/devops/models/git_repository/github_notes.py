from django.db import models

from core.models.model_notes import ModelNotes

from devops.models.git_repository.github import GitHubRepository



class GitHubRepositoryNotes(
    ModelNotes
):


    class Meta:

        db_table = 'devops_github_repository_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'GitHub Repository Note'

        verbose_name_plural = 'GitHub Repository Notes'


    model = models.ForeignKey(
        GitHubRepository,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'notes',
        verbose_name = 'Model',
    )

    app_namespace = 'devops'

    table_fields: list = []

    page_layout: dict = []


    def get_url_kwargs(self) -> dict:

        return {
            'model_id': self.model.pk,
            'pk': self.pk
        }
