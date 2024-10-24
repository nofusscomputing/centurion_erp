from django.contrib.auth.models import User
from django.db import models

from access.fields import AutoCreatedField

from .projects import Project, ProjectCommonFieldsName, SaveHistory



class ProjectMilestone(ProjectCommonFieldsName):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = 'Project Milestone'

        verbose_name_plural = 'Project Milestones'


    description = models.TextField(
        blank = True,
        default = None,
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
        on_delete=models.CASCADE,
        null = False,
    )

    model_notes = None


    created = AutoCreatedField(
        editable = False,
    )


    def __str__(self):

        return self.name


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.project


    @property
    def percent_completed(self) -> str: # Auto-Calculate
        """ How much of the milestone is completed.

        Returns:
            str: Calculated percentage of project completion.
        """

        return 'xx %'
