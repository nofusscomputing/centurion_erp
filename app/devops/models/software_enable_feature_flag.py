from datetime import date, datetime
from django.db import models

from rest_framework.reverse import reverse

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject

from core.lib.feature_not_used import FeatureNotUsed

from devops.models.check_ins import CheckIn

from itam.models.software import Software



class SoftwareEnableFeatureFlag(
    TenancyObject
):

    save_model_history: bool = False


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

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    is_global = None    # Field not requied.

    model_notes = None


    def __str__(self) -> str:

        enabled = 'Disabled'

        if self.enabled:

            enabled = 'Enabled'

        return str(enabled)

    documentation = ''

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
            created__date = datetime.now().date()
        )

        unique_deployment = {}

        for deployment in checkin:

            if unique_deployment.get(deployment.deployment_id, None) is None:

                unique_deployment.update({
                    deployment.deployment_id: 1
                })


        return len(unique_deployment)


    def get_url_kwargs(self) -> dict:

        return {
            'software_id': self.software.pk,
            'pk': self.pk
        }

    
    def get_url( self, request = None ) -> str:

        if request:

            return reverse(f"v2:" + self.get_app_namespace() + f"_api_v2_feature_flag_software-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:" + self.get_app_namespace() + f"_api_v2_feature_flag_software-detail", kwargs = self.get_url_kwargs() )



    def get_url_kwargs_notes(self):

        return FeatureNotUsed
