import django
from django.db import models

from access.fields import *
from access.models.team import Team
from access.models.tenancy import TenancyObject

from assistance.models.knowledge_base_category import KnowledgeBaseCategory

User = django.contrib.auth.get_user_model()



class KnowledgeBase(TenancyObject):


    class Meta:

        ordering = [
            'title',
        ]

        verbose_name = "Knowledge Base"

        verbose_name_plural = "Knowledge Base Articles"


    model_notes = None


    id = models.AutoField(
        blank=False,
        help_text = 'ID of this KB article',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )


    title = models.CharField(
        blank = False,
        help_text = 'Title of the article',
        max_length = 50,
        unique = False,
        verbose_name = 'Title',
    )


    summary = models.TextField(
        blank = True,
        default = None,
        help_text = 'Short Summary of the article',
        null = True,
        verbose_name = 'Summary',
    )


    content = models.TextField(
        blank = True,
        default = None,
        help_text = 'Content of the article. Markdown is supported',
        null = True,
        verbose_name = 'Article Content',
    )


    category = models.ForeignKey(
        KnowledgeBaseCategory,
        blank = False,
        default = None,
        help_text = 'Article Category',
        max_length = 50,
        null = True,
        on_delete = models.SET_NULL,
        unique = False,
        verbose_name = 'Category',
    )


    release_date = models.DateTimeField(
        blank = True,
        default = None,
        help_text = 'Date the article will be published',
        null = True,
        verbose_name = 'Publish Date',
    )


    expiry_date = models.DateTimeField(
        blank = True,
        default = None,
        help_text = 'Date the article will be removed from published articles',
        null = True,
        verbose_name = 'End Date',
    )


    target_team = models.ManyToManyField(
        Team,
        blank = True,
        default = None,
        help_text = 'Team(s) to grant access to the article',
        verbose_name = 'Target Team(s)',
    )


    target_user = models.ForeignKey(
        User,
        blank = True,
        default = None,
        help_text = 'User(s) to grant access to the article',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Target Users(s)',
    )


    responsible_user = models.ForeignKey(
        User,
        blank = False,
        default = None,
        help_text = 'User(s) whom is considered the articles owner.',
        null = True,
        on_delete = models.SET_NULL,
        related_name = 'responsible_user',
        verbose_name = 'Responsible User',
    )


    responsible_teams = models.ManyToManyField(
        Team,
        blank = True,
        default = None,
        help_text = 'Team(s) whom is considered the articles owner.',
        related_name = 'responsible_teams',
        verbose_name = 'Responsible Team(s)',
    )


    public = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this article to be made available publically',
        verbose_name = 'Public Article',
    )


    created = AutoCreatedField()


    modified = AutoLastModifiedField()


    page_layout: dict = [
        {
            "name": "Content",
            "slug": "content",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        'summary',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'content',
                    ]
                }
            ]
        },
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'title',
                        'category',
                        'responsible_user',
                        'responsible_teams',
                        'is_global',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                        'release_date',
                        'expiry_date',
                        'target_user',
                        'target_team',
                    ]
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
        'title',
        'category',
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return self.title


    def save_history(self, before: dict, after: dict) -> bool:

        from assistance.models.knowledge_base_history import KnowledgeBaseHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = KnowledgeBaseHistory,
        )


        return history
