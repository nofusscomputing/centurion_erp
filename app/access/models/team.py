from django.db import models
from django.contrib.auth.models import Group

from rest_framework.reverse import reverse

from access.fields import (
    AutoCreatedField,
    AutoLastModifiedField
)

from access.models.organization import Organization
from access.models.tenancy import TenancyObject

from core import exceptions as centurion_exceptions


class Team(Group, TenancyObject):

    class Meta:

        ordering = [ 'team_name' ]

        verbose_name = 'Team'

        verbose_name_plural = "Teams"


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.name = self.organization.name.lower().replace(' ', '_') + '_' + self.team_name.lower().replace(' ', '_')

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


    def validatate_organization_exists(self):
        """Ensure that the user did provide an organization

        Raises:
            ValidationError: User failed to supply organization.
        """

        if not self:
            raise centurion_exceptions.ValidationError('You must provide an organization')



    team_name = models.CharField(
        blank = False,
        help_text = 'Name to give this team',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    organization = models.ForeignKey(
        Organization,
        blank = False,
        help_text = 'Organization this belongs to',
        null = False,
        on_delete = models.CASCADE,
        validators = [validatate_organization_exists],
        verbose_name = 'Organization'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'team_name',
                        'created',
                        'modified',
                    ],
                    "right": [
                        'model_notes',
                    ]
                },
                {
                    "layout": "table",
                    "name": "Users",
                    "field": "users",
                },
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
        'team_name',
        'modified',
        'created',
    ]


    def get_url( self, request = None ) -> str:

        if request:

            return reverse(f"v2:_api_v2_organization_team-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:_api_v2_organization_team-detail", kwargs = self.get_url_kwargs() )


    def get_url_kwargs(self) -> dict:
        """Fetch the URL kwargs

        Returns:
            dict: kwargs required for generating the URL with `reverse`
        """

        return {
            'organization_id': self.organization.id,
            'pk': self.id
        }


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.organization


    def permission_list(self) -> list:

        permission_list = []

        for permission in self.permissions.all():

            if str(permission.content_type.app_label + '.' + permission.codename) in permission_list:
                continue

            permission_list += [ str(permission.content_type.app_label + '.' + permission.codename) ]

        return [permission_list, self.permissions.all()]


    def __str__(self):
        return self.organization.name + ', ' + self.team_name
