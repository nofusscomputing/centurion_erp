from django.db import models

from devops.models.git_repository.base import GitRepository



class GitHubRepository(
    GitRepository
):
    """GitHub Repository"""

    class Meta(GitRepository.Meta):

        verbose_name = 'GitHub Repository'

        verbose_name_plural = 'GitHub Repositories'


    wiki = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Enable Wiki',
        verbose_name = 'Wiki'
    )

    issues = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Enable Issues',
        verbose_name = 'Issues'
    )

    sponsorships = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Enable Sponsorships',
        verbose_name = 'Sponsorships'
    )

    preserve_this_repository = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Enable Preservation of this repository',
        verbose_name = 'Preserve This Repository'
    )

    discussions = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Enable Discussions',
        verbose_name = 'Discussions'
    )

    projects = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Enable Projects',
        verbose_name = 'Projects'
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
                        'wiki',
                        'issues',
                        'sponsorships',
                    ],
                    "right": [
                        'preserve_this_repository',
                        'discussions',
                        'projects',
                    ]
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

    # table_fields: list = [
    #     'name',
    #     'provider',
    #     'path',
    #     'organization',
    #     'created',
    # ]

    def get_url_kwargs_notes(self) -> dict:
        """Fetch the URL kwargs for model notes

        Returns:
            dict: notes kwargs required for generating the URL with `reverse`
        """

        return {
            'model_id': self.id
        }
 
    def save_history(self, before: dict, after: dict) -> bool:

        from devops.models.git_repository.github_history import GitHubHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = GitHubHistory
        )


        return history
