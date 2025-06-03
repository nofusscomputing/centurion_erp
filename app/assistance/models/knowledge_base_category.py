import django
from django.db import models

from access.fields import *
from access.models.team import Team

from core.models.centurion import CenturionModel

User = django.contrib.auth.get_user_model()



class KnowledgeBaseCategory(
    CenturionModel
):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Knowledge Base Category"

        verbose_name_plural = "Knowledge Base Categories"


    parent_category = models.ForeignKey(
        'self',
        blank = True,
        default = None,
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
        'is_global',
        'organization',
    ]


    def __str__(self):

        return self.name
