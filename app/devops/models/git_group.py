from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject


class GitGroup(
    TenancyObject
):


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

    id = models.AutoField(
        blank=False,
        help_text = 'Primary key of the entry',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    parent_group = models.ForeignKey(
        'self',
        blank = True,
        default = None,
        help_text = 'Parent Git Group this repository belongs to.',
        on_delete = models.PROTECT,
        null = True,
        related_name = '+',
        verbose_name = 'Parent Group',
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

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def __str__(self) -> str:

        if self.parent_group:

            return str(self.parent_group) + '/' + self.path

        return self.path


    @property
    def provider_badge(self):

        from core.classes.badge import Badge

        text: str = self.get_provider_display()

        return Badge(
            icon_name = f'{text.lower()}',
            icon_style = f'badge-icon-action-{text.lower()}',
            text = text,
        )


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        if self.parent_group:

            self.organization = self.parent_group.organization

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    app_namespace = 'devops'

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

    def save_history(self, before: dict, after: dict) -> bool:

        from devops.models.git_group_history import GitGroupHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = GitGroupHistory
        )


        return history
