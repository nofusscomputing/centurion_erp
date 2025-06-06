from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject

from assistance.models.knowledge_base import KnowledgeBase



class ProjectTypeCommonFields(TenancyObject):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'Type ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class ProjectType(ProjectTypeCommonFields):


    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = "Project Type"

        verbose_name_plural = "Project Types"


    name = models.CharField(
        blank = False,
        help_text = "Name of thee project type.",
        max_length = 50,
        unique = True,
        verbose_name = 'Name',
    )

    runbook = models.ForeignKey(
        KnowledgeBase,
        blank= True,
        help_text = 'The runbook for this project type',
        null = True,
        on_delete = models.SET_NULL,
        verbose_name = 'Runbook',
    )


    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'name'
                        'runbook',
                    ],
                    "right": [
                        'model_notes'
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

    def save_history(self, before: dict, after: dict) -> bool:

        from project_management.models.project_type_history import ProjectTypeHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = ProjectTypeHistory,
        )


        return history
