from django.core.exceptions import (
    ValidationError
)
from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel


class GitGroup(
    CenturionModel
):


    app_namespace = 'devops'

    documentation = ''

    model_tag = 'git_group'

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
                        'parent_group',
                        'path',
                        'name',
                    ],
                    "right": [
                        'model_notes',
                        'description',
                        'provider_pk',
                        'created',
                        'modified',
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

    table_fields: list = [
        'name',
        'provider_badge',
        'path',
        'organization',
        'created',
    ]


    class Meta:

        ordering = [
            'organization',
            'path',
            'name',
        ]

        # unique_together = [    # Cant use until import is a feature
        #     'provider',
        #     'provider_pk'
        # ]

        verbose_name = 'GIT Group'

        verbose_name_plural = 'GIT Groups'


    class GitProvider(models.IntegerChoices):

        GITHUB = 1, 'GitHub'
        GITLAB = 2, 'GitLab'



    is_global = None

    parent_group = models.ForeignKey(
        'self',
        blank = True,
        help_text = 'Parent Git Group this repository belongs to.',
        on_delete = models.PROTECT,
        null = True,
        related_name = '+',
        verbose_name = 'Parent Group',
    )


    @property
    def provider_badge(self):

        from core.classes.badge import Badge

        text: str = self.get_provider_display()

        return Badge(
            icon_name = f'{text.lower()}',
            icon_style = f'badge-icon-action-{text.lower()}',
            text = text,
        )


    provider = models.IntegerField(
        blank = False,
        choices = GitProvider,
        help_text = 'GIT Provider for this Group',
        verbose_name = 'Git Provider'
    )

    provider_pk = models.IntegerField(
        blank = True,
        help_text = 'Providers ID for this Group',
        null = True,
        unique = False,
        verbose_name = 'Provider ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Group',
        max_length = 80,
        null = False,
        unique = False,
        verbose_name = 'Name'
    )

    path = models.CharField(
        blank = False,
        help_text = 'Path of the group',
        max_length = 80,
        null = False,
        unique = False,
        verbose_name = 'Path'
    )

    description = models.TextField(
        blank = True,
        help_text = 'Description for this group',
        max_length = 300,
        null = True,
        verbose_name = 'Description'
    )

    modified = AutoLastModifiedField()


    def __str__(self) -> str:

        if self.parent_group:

            return str(self.parent_group) + '/' + self.path

        return self.path



    def clean_fields(self, exclude = None):

        if self.parent_group:

            if self.provider == self.GitProvider.GITHUB:

                raise ValidationError(
                    code = 'no_parent_for_github_group',
                    message = 'Github Organizations cant be assigned a parent group',
                    params = {
                        'field': 'parent_group'
                    }
                )

            self.organization = self.parent_group.organization

        super().clean_fields( exclude = exclude )
