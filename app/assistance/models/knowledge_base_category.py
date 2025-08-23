from django.conf import settings
from django.contrib.auth.models import Group
from django.db import models

from access.fields import *

from core.models.centurion import CenturionModel



class KnowledgeBaseCategory(
    CenturionModel
):

    model_tag = 'kb_category'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Knowledge Base Category"

        verbose_name_plural = "Knowledge Base Categories"


    parent_category = models.ForeignKey(
        'self',
        blank = True,
        help_text = 'Category this category belongs to',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Parent Category',
    )


    name = models.CharField(
        blank = False,
        help_text = 'Name/Title of the Category',
        max_length = 50,
        unique = False,
        verbose_name = 'Title',
    )

    target_team = models.ManyToManyField(
        Group,
        blank = True,
        help_text = 'Group(s) to grant access to the article',
        related_name = '+',
        verbose_name = 'Target Group(s)',
    )


    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = True,
        help_text = 'User(s) to grant access to the article',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Target Users(s)',
    )


    modified = AutoLastModifiedField()


    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'parent_category',
                        'name',
                        'target_user',
                        'target_team',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
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
        'name',
        'parent_category',
        'organization',
    ]


    def __str__(self):

        return self.name
