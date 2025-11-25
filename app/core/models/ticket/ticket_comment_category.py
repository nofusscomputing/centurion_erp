from django.db import models

from access.fields import AutoLastModifiedField

from assistance.models.knowledge_base import KnowledgeBase

from core.models.centurion import CenturionModel



class TicketCommentCategory(
    CenturionModel,
):

    model_tag = 'ticket_comment_category'


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = "Ticket Comment Category"

        verbose_name_plural = "Ticket Comment Categories"


    parent = models.ForeignKey(
        'self',
        blank = True,
        help_text = 'The Parent Category',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Parent Category',
    )

    name = models.CharField(
        blank = False,
        help_text = "Category Name",
        max_length = 50,
        verbose_name = 'Name',
    )

    runbook = models.ForeignKey(
        KnowledgeBase,
        blank = True,
        help_text = 'The runbook for this category',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Runbook',
    )

    comment = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for standard comment',
        null = False,
        verbose_name = 'Comment',
    )

    notification = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for notification comment',
        null = False,
        verbose_name = 'Notification Comment',
    )

    solution = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for solution comment',
        null = False,
        verbose_name = 'Solution Comment',
    )

    task = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for task comment',
        null = False,
        verbose_name = 'Task Comment',
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
                        'name',
                        'is_global',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
                {
                    "layout": "double",
                    "name": "Comment Types",
                    "left": [
                        'comment',
                        'notification',
                    ],
                    "right": [
                        'solution',
                        'task',
                    ]
                },
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
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return self.name
