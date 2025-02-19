from django.db import models

from rest_framework.reverse import reverse

from access.models.team import Team

from core.models.model_notes import ModelNotes



class TeamNotes(
    ModelNotes
):


    class Meta:

        db_table = 'access_team_notes'

        ordering = ModelNotes._meta.ordering

        verbose_name = 'Team Note'

        verbose_name_plural = 'Team Notes'


    model = models.ForeignKey(
        Team,
        blank = False,
        help_text = 'Model this note belongs to',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'notes',
        verbose_name = 'Model',
    )

    table_fields: list = []

    page_layout: dict = []


    def get_url( self, request = None ) -> str:

        kwargs = {
            'organization_id': self.organization.pk,
            'model_id': self.model.pk,
            'pk': self.pk
        }

        if request:

            return reverse("v2:_api_v2_organization_team_note-detail", request=request, kwargs = kwargs )

        return reverse("v2:_api_v2_organization_team_note-detail", kwargs = kwargs )
