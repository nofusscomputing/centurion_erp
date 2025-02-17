from django.db import models

from core.models.model_history import ModelHistory

from project_management.models.projects import Project



class ProjectHistory(
    ModelHistory
):


    class Meta:

        db_table = 'project_management_project_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Project History'

        verbose_name_plural = 'Project History'


    model = models.ForeignKey(
        Project,
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

        from project_management.serializers.project import ProjectBaseSerializer

        model = ProjectBaseSerializer(self.model, context = serializer_context)

        return model
