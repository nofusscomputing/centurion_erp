from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group

from rest_framework.reverse import reverse

from access.fields import (
    AutoCreatedField,
    AutoLastModifiedField
)

from access.models.organization import Organization
from access.models.team import Team

from core.lib.feature_not_used import FeatureNotUsed
from core.mixin.history_save import SaveHistory



class TeamUsers(SaveHistory):

    class Meta:

        ordering = ['user']

        verbose_name = "Team User"

        verbose_name_plural = "Team Users"


    id = models.AutoField(
        blank=False,
        help_text = 'ID of this Team User',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    team = models.ForeignKey(
        Team,
        blank = False,
        help_text = 'Team user belongs to',
        null = False,
        on_delete=models.CASCADE,
        related_name="team",
        verbose_name = 'Team'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank = False,
        help_text = 'User who will be added to the team',
        null = False,
        on_delete=models.CASCADE,
        verbose_name = 'User'
    )

    manager = models.BooleanField(
        blank=True,
        default=False,
        help_text = 'Is this user to be a manager of this team',
        verbose_name='manager',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    page_layout: list = []

    table_fields: list = [
        'user',
        'manager'
    ]

    history_app_label: str = None
    history_model_name: str = None
    kb_model_name: str = None
    note_basename: str = None


    def delete(self, using=None, keep_parents=False):
        """ Delete Team

        Overrides, post-action
            As teams are an extension of Groups, remove the user to the team.
        """

        super().delete(using=using, keep_parents=keep_parents)

        group = Group.objects.get(pk=self.team.id)

        user = User.objects.get(pk=self.user_id)
        
        user.groups.remove(group)


    def get_organization(self) -> Organization:
        return self.team.organization


    def get_url( self, request = None ) -> str:

        url_kwargs: dict = {
            'organization_id': self.team.organization.id,
            'team_id': self.team.id,
            'pk': self.id
        }

        print(f'url kwargs are: {url_kwargs}')


        if request:

            return reverse(f"v2:_api_v2_organization_team_user-detail", request=request, kwargs = url_kwargs )

        return reverse(f"v2:_api_v2_organization_team_user-detail", kwargs = url_kwargs )


    def get_url_kwargs_notes(self):

        return FeatureNotUsed


    def save(self, *args, **kwargs):
        """ Save Team

        Overrides, post-action
            As teams are an extension of groups, add the user to the matching group.
        """

        super().save(*args, **kwargs)

        group = Group.objects.get(pk=self.team.id)

        user = User.objects.get(pk=self.user_id)

        user.groups.add(group) 


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.team

    def __str__(self):
        return self.user.username
