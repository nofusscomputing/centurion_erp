from django.db import models

from devops.models.git_repository.base import GitRepository



class GitLabRepository(
    GitRepository,
):
    """GitLab Repository"""

    _is_submodel = True

    documentation = ''


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
