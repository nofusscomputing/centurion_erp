import django

from django.conf import settings
from django.db import models
from django.contrib.auth.models import Group

from access.fields import (
    AutoLastModifiedField
)

from access.models.tenant import Tenant
from access.models.team import Team

from core.models.centurion import CenturionModel

User = django.contrib.auth.get_user_model()



class TeamUsers(
    CenturionModel
):

    _audit_enabled = False

    _notes_enabled = False

    organization = None    # Dont add organization field

    class Meta:

        ordering = ['user']

        verbose_name = "Team User"

        verbose_name_plural = "Team Users"

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

    modified = AutoLastModifiedField()

    page_layout: list = []

    table_fields: list = [
        'user',
        'manager'
    ]


    def delete(self, using=None, keep_parents=False):
        """ Delete Team

        Overrides, post-action
            As teams are an extension of Groups, remove the user to the team.
        """

        super().delete(using=using, keep_parents=keep_parents)

        group = Group.objects.get(pk=self.team.id)

        user = User.objects.get(pk=self.user_id)
        
        user.groups.remove(group)


    def get_organization(self) -> Tenant:
        return self.team.organization


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs()

        kwargs.update({
            'organization_id': self.team.organization.id,
            'team_id': self.team.id
        })

        return kwargs


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
