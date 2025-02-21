from django.db import models

from core.models.model_history import ModelHistory

from access.models.team import Team



class TeamHistory(
    ModelHistory
):


    class Meta:

        db_table = 'access_team_history'

        ordering = ModelHistory._meta.ordering

        verbose_name = 'Team History'

        verbose_name_plural = 'Team History'


    model = models.ForeignKey(
        Team,
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

        from access.serializers.teams import TeamBaseSerializer

        model = TeamBaseSerializer(self.model, context = serializer_context)

        return model
