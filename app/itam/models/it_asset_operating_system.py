from django.db import models

from core.mixins.centurion import Centurion



class ITAssetOperatingSystem(
    Centurion,
):
    """Custom M2M Table

    This table tracks the date the OS was first detected.
    """

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False

    model_tag = None


    class Meta:

        ordering = [
            'installed',
        ]

        verbose_name = 'IT Asset Operating System'

        verbose_name_plural = 'IT Asset Operating Systems'

    it_asset = models.ForeignKey(
        to = 'itam.ITAsset',
        blank = True,
        help_text = 'Asset OS installed upon.',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'IT Asset'
    )


    installed = models.DateTimeField(
        blank = True,
        help_text = 'Initial date the OS was detected.',
        null = True,
        verbose_name = 'Date Detected',
    )


    operating_system_version = models.ForeignKey(
        to = 'itam.OperatingSystemVersion',
        blank = True,
        help_text = 'Asset OS installed upon.',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'it_asset',
        verbose_name = 'Operating System Version'
    )


    @property
    def operating_system(self):

        return self.operating_system_version.operating_system


    page_layout: dict = {
        "table": [
            'it_asset',
            'installed',
            'operating_system',
            'operating_system_version',
        ]
    }

    def get_tenant(self):
        return self.it_asset.organization


    def get_url_kwargs(self, many=False) -> dict:
        kwargs = super().get_url_kwargs(many)

        kwargs['model_name'] = self.it_asset._meta.model_name
        kwargs['model_id'] = self.it_asset.id
        kwargs['related_model_name'] = 'operating_system'

        return kwargs
