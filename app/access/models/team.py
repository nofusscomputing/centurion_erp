from django.db import models
from django.contrib.auth.models import Group

from access.fields import (
    AutoLastModifiedField
)

from core.models.centurion import CenturionModel



class Team(
    Group,
    CenturionModel,
):


    class Meta:

        ordering = [ 'team_name' ]

        verbose_name = 'Team'

        verbose_name_plural = "Teams"


    team_name = models.CharField(
        blank = False,
        help_text = 'Name to give this team',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

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



    def clean_fields(self, exclude = None):

        if self.organization_id:

            self.name = self.organization.name.lower().replace(' ', '_') + '_' + self.team_name.lower().replace(' ', '_')


        super().clean_fields(exclude = exclude)



    def permission_list(self) -> list:

        permission_list = []

        for permission in self.permissions.all():

            if str(permission.content_type.app_label + '.' + permission.codename) in permission_list:
                continue

            permission_list += [ str(permission.content_type.app_label + '.' + permission.codename) ]

        return [permission_list, self.permissions.all()]


    def __str__(self):
        return self.organization.name + ', ' + self.team_name
