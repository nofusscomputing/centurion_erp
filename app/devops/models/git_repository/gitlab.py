from django.db import models

from devops.models.git_repository.base import GitRepository



class GitLabRepository(
    GitRepository
):
    """GitLab Repository"""

    class Meta(GitRepository.Meta):

        verbose_name = 'GitLab Repository'

        verbose_name_plural = 'GitLab Repositories'


    class RepositoryVisibility(models.IntegerChoices):

        PRIVATE  = 1, 'Private'
        INTERNAL = 2, 'Internal'
        PUBLIC   = 3, 'Public'


    visibility = models.IntegerField(
        blank = False,
        choices = RepositoryVisibility,
        help_text = 'Visibility of this repository',
        null = False,
        verbose_name = 'Visibility',
    )


    documentation = ''

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'provider',
                        'git_group',
                        'path',
                        'name',
                    ],
                    "right": [
                        'model_notes',
                        'description',
                        'provider_id',
                        'created',
                        'modified',
                    ]
                },
                {
                    "name": "Settings",
                    "layout": "double",
                    "left": [
                        'visibility',
                    ],
                    "right": []
                }
            ]
        },
        {
            "name": "Knowledge Base",
            "slug": "kb_articles",
            "sections": [
                {
                    "layout": "table",
                    "field": "knowledge_base",
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]

    def get_url_kwargs_notes(self) -> dict:
        """Fetch the URL kwargs for model notes

        Returns:
            dict: notes kwargs required for generating the URL with `reverse`
        """

        return {
            'model_id': self.id
        }
 
    def save_history(self, before: dict, after: dict) -> bool:

        from devops.models.git_repository.gitlab_history import GitlabHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = GitlabHistory
        )


        return history
