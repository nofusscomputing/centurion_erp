import pytz

from datetime import datetime

from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from devops.models.check_ins import CheckIn

from itam.models.software import Software



class SoftwareEnableFeatureFlag(
    CenturionModel
):

    _audit_enabled = False

    _notes_enabled = False

    documentation = ''


    class Meta:

        ordering = [
            'software',
            'organization'
        ]

        unique_together = [
            'organization',
            'software',
        ]

        verbose_name = 'Software Feature Flagging'

        verbose_name_plural = 'Software Feature Flaggings'


    software = models.ForeignKey(
        Software,
        blank = False,
        help_text = 'Software this feature flag is for',
        on_delete = models.PROTECT,
        null = False,
        related_name = 'feature_flagging',
        verbose_name = 'Software'
    )

    enabled = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is feature flagging enabled for this software',
        verbose_name = 'Enabled'
    )

    modified = AutoLastModifiedField()

    model_notes = None


    def __str__(self) -> str:

        enabled = 'Disabled'

        if self.enabled:

            enabled = 'Enabled'

        return str(enabled)

    page_layout: dict = []


    table_fields: list = [
        # {
        #     "field": "display_name",
        #     "type": "link",
        #     "key": "_self"
        # },
        'display_name',
        'organization',
        'checkins',
        'created',
        '-action_delete-',
    ]

    @property
    def get_daily_checkins(self):

        checkin = CheckIn.objects.filter(
            organization = self.organization,
            feature = 'feature_flag',
            software = self.software,
            created__range = (
                datetime.fromtimestamp(datetime.utcnow().timestamp() - 86400, pytz.timezone('utc')), 
                datetime.fromtimestamp(datetime.utcnow().timestamp(), pytz.timezone('utc'))
            )
        )

        unique_deployment = {}

        for deployment in checkin:

            if unique_deployment.get(deployment.deployment_id, None) is None:

                unique_deployment.update({
                    deployment.deployment_id: 1
                })


        return len(unique_deployment)


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many )
        kwargs.update({
            'software_id': self.software.pk,
        })

        return kwargs
