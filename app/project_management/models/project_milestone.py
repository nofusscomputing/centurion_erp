from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from .projects import Project



class ProjectMilestone(
    CenturionModel
):

    model_tag = 'project_milestone'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Project Milestone'

        verbose_name_plural = 'Project Milestones'


    name = models.CharField(
        blank = False,
        help_text = 'Name of the item',
        max_length = 100,
        unique = True,
        verbose_name = 'Name'
    )

    description = models.TextField(
        blank = True,
        help_text = 'Description of milestone. Markdown supported',
        null= True,
        verbose_name = 'Description',
    )

    start_date = models.DateTimeField(
        blank = True,
        help_text = 'When work commenced on the project.',
        null = True,
        verbose_name = 'Real Start Date',
    )

    finish_date = models.DateTimeField(
        blank = True,
        help_text = 'When work was completed for the project',
        null = True,
        verbose_name = 'Real Finish Date',
    )

    project = models.ForeignKey(
        Project,
        blank= False,
        help_text = 'Project this milestone belongs.',
        on_delete = models.CASCADE,
        null = False,
    )

    model_notes = None

    modified = AutoLastModifiedField()


    # model not intended to be vieable on its own page
    # as this model is a sub-model.
    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'project',
                        'name',
                        'start_date',
                        'finish_date',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'description',
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
            "name": "Tickets",
            "slug": "tickets",
            "sections": [
                # {
                #     "layout": "table",
                #     "field": "tickets",
                # }
            ],
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]


    table_fields: list = [
        'name',
        'percent_completed'
        'start_date',
        'finish_date',
    ]


    def __str__(self):

        return self.name


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        kwargs.update({
            'project_id': self.project.id
        })

        return kwargs


    @property
    def percent_completed(self) -> str: # Auto-Calculate
        """ How much of the milestone is completed.

        Returns:
            str: Calculated percentage of project completion.
        """

        return 'xx %'

    def save_history(self, before: dict, after: dict) -> bool:

        from project_management.models.project_milestone_history import ProjectMilestoneHistory

        history = super().save_history(
            before = before,
            after = after,
            history_model = ProjectMilestoneHistory,
        )


        return history
