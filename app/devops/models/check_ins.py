from django.db import models

from access.fields import AutoCreatedField
from access.models.tenancy import TenancyObject

from itam.models.software import Software



class CheckIn(
    TenancyObject
):

    save_model_history: bool = False

    class Meta:

        ordering = [
            'organization',
            'software',
            'feature',
        ]

        verbose_name = 'Deployment Check In'

        verbose_name_plural = 'Deployment Check Ins'


    id = models.AutoField(
        blank=False,
        help_text = 'Primary key of the entry',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    software = models.ForeignKey(
        Software,
        blank = False,
        help_text = 'Software related to the checkin',
        on_delete = models.CASCADE,
        related_name = '+',
        verbose_name = 'Software',
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

    created = AutoCreatedField()

    is_global = None      # Field not requied.
    model_notes = None    # Field not required.


    def __str__(self) -> str:

        return self.feature + '.' + self.deployment_id

    app_namespace = 'devops'

    documentation = ''

    page_layout: dict = []


    table_fields: list = [
        'software',
        'feature',
        'deployment_id',
        'organization',
        'created',
    ]
