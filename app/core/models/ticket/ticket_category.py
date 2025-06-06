from django.db import models

from access.fields import AutoLastModifiedField

from assistance.models.knowledge_base import KnowledgeBase

from core.models.centurion import CenturionModel



class TicketCategory(
    CenturionModel,
):


    class Meta:

        ordering = [
            'parent__name',
            'name',
        ]

        verbose_name = "Ticket Category"

        verbose_name_plural = "Ticket Categories"


    parent = models.ForeignKey(
        'self',
        blank= True,
        help_text = 'The Parent Category',
        null = True,
        on_delete = models.SET_NULL,
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
        blank= True,
        help_text = 'The runbook for this category',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Runbook',
    )

    change = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for change tickets',
        null = False,
        verbose_name = 'Change Tickets',
    )

    incident = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for incident tickets',
        null = False,
        verbose_name = 'Incident Tickets',
    )

    problem = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for problem tickets',
        null = False,
        verbose_name = 'Problem Tickets',
    )

    project_task = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for Project tasks',
        null = False,
        verbose_name = 'Project Tasks',
    )

    request = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'Use category for request tickets',
        null = False,
        verbose_name = 'Request Tickets',
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
                        'parent'
                        'name'
                        'runbook',
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
                    "left": [
                        'change',
                        'problem'
                        'request'
                    ],
                    "right": [
                        'incident',
                        'project_task',
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
        'organization',
        'created',
        'modified'
    ]


    @property
    def recusive_name(self):

        if self.parent:

            return str(self.parent.recusive_name + ' > ' + self.name )

        return self.name

    def __str__(self):

        return self.recusive_name
