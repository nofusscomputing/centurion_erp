from django.db import models

from core.models.model_notes import ModelNotes

from devops.models.git_repository.gitlab import GitLabRepository



class GitLabRepositoryNotes(
    ModelNotes
):


    class Meta:

        db_table = 'devops_gitlab_repository_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'GitLab Repository Note'

        verbose_name_plural = 'GitLab Repository Notes'


    model = models.ForeignKey(
        GitLabRepository,
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
