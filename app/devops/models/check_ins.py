from django.db import models

from core.models.centurion import CenturionModel

from itam.models.software import Software



class CheckIn(
    CenturionModel
):

    _audit_enabled = False

    _notes_enabled = False

    app_namespace = 'devops'

    documentation = ''

    class Meta:

        ordering = [
            'organization',
            'software',
            'feature',
        ]

        verbose_name = 'Deployment Check In'

        verbose_name_plural = 'Deployment Check Ins'


    software = models.ForeignKey(
        Software,
        blank = False,
        help_text = 'Software related to the checkin',
        on_delete = models.CASCADE,
        related_name = '+',
        verbose_name = 'Software',
    )

    version = models.TextField(
        blank = True,
        help_text = 'Version of the deployed software',
        max_length = 80,
        null = True,
        unique = False,
        verbose_name = 'Deployed Version'
    )

    deployment_id = models.CharField(
        blank = False,
        help_text = 'Unique Deployment ID',
        max_length = 64,
        unique = False,
        verbose_name = 'Deployment ID'
    )

    feature = models.TextField(
        blank = False,
        help_text = 'Feature that was checked into',
        max_length = 30,
        null = False,
        unique = False,
        verbose_name = 'Feature'
    )

    model_notes = None    # Field not required.


    def __str__(self) -> str:

        return self.feature + '.' + self.deployment_id

    page_layout: dict = []


    table_fields: list = [
        'software',
        'feature',
        'deployment_id',
        'organization',
        'created',
    ]
