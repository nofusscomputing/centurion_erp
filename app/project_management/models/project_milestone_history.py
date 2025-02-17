from django.db import models

from core.models.model_history import ModelHistory

from project_management.models.project_milestone import ProjectMilestone



class ProjectMilestoneHistory(
    ModelHistory
):


    class Meta:

        db_table = 'project_management_projectmilestone_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Project Milestone History'

        verbose_name_plural = 'Project Milestone History'


    model = models.ForeignKey(
        ProjectMilestone,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'history',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_object(self):

        return self


    def get_serialized_model(self, serializer_context):

        model = None

        from project_management.serializers.project_milestone import ProjectMilestoneBaseSerializer

        model = ProjectMilestoneBaseSerializer(self.model, context = serializer_context)

        return model
