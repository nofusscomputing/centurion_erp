import django
from django.db import models

from access.fields import *
from access.models.team import Team

from assistance.models.knowledge_base_category import KnowledgeBaseCategory

from core.models.centurion import CenturionModel

User = django.contrib.auth.get_user_model()



class KnowledgeBase(
    CenturionModel
):

    model_tag = 'kb'


    class Meta:

        ordering = [
            'title',
        ]

        verbose_name = "Knowledge Base"

        verbose_name_plural = "Knowledge Base Articles"


    title = models.CharField(
        blank = False,
        help_text = 'Title of the article',
        max_length = 50,
        unique = False,
        verbose_name = 'Title',
    )


    summary = models.TextField(
        blank = True,
        help_text = 'Short Summary of the article',
        null = True,
        verbose_name = 'Summary',
    )


    content = models.TextField(
        blank = True,
        help_text = 'Content of the article. Markdown is supported',
        null = True,
        verbose_name = 'Article Content',
    )


    category = models.ForeignKey(
        KnowledgeBaseCategory,
        blank = False,
        help_text = 'Article Category',
        max_length = 50,
        null = True,
        on_delete = models.PROTECT,
        unique = False,
        verbose_name = 'Category',
    )


    release_date = models.DateTimeField(
        blank = True,
        help_text = 'Date the article will be published',
        null = True,
        verbose_name = 'Publish Date',
    )


    expiry_date = models.DateTimeField(
        blank = True,
        help_text = 'Date the article will be removed from published articles',
        null = True,
        verbose_name = 'End Date',
    )


    target_team = models.ManyToManyField(
        Team,
        blank = True,
        help_text = 'Team(s) to grant access to the article',
        verbose_name = 'Target Team(s)',
    )


    target_user = models.ForeignKey(
        User,
        blank = True,
        help_text = 'User(s) to grant access to the article',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Target Users(s)',
    )


    responsible_user = models.ForeignKey(
        User,
        blank = False,
        help_text = 'User(s) whom is considered the articles owner.',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'responsible_user',
        verbose_name = 'Responsible User',
    )


    responsible_teams = models.ManyToManyField(
        Team,
        blank = True,
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
