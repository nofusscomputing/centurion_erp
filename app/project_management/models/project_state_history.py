from django.db import models

from core.models.model_history import ModelHistory

from project_management.models.project_states import ProjectState



class ProjectStateHistory(
    ModelHistory
):


    class Meta:

        db_table = 'project_management_projectstate_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Project State History'

        verbose_name_plural = 'Project State History'


    model = models.ForeignKey(
        ProjectState,
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

        from project_management.serializers.project_states import ProjectStateBaseSerializer

        model = ProjectStateBaseSerializer(self.model, context = serializer_context)

        return model
