from django.db import models

from access.fields import AutoLastModifiedField

from assistance.models.knowledge_base import KnowledgeBase

from core.models.centurion import CenturionModel



class ProjectState(
    CenturionModel
):

    model_tag = 'project_state'


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = "Project State"

        verbose_name_plural = "Project States"


    name = models.CharField(
        blank = False,
        help_text = "Name of thee project state.",
        max_length = 50,
        unique = True,
        verbose_name = 'Name',
    )

    runbook = models.ForeignKey(
        KnowledgeBase,
        blank = True,
        help_text = 'The runbook for this project state',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Runbook',
    )


    is_completed = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this state considered complete',
        null = False,
        verbose_name = 'State Completed',
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
                        'runbook',
                        'is_completed',
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
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return self.name
