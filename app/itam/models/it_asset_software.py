from django.db import models

from core.mixins.centurion import Centurion



class ITAssetSoftware(
    Centurion,
):
    """Custom M2M Table

    This table tracks the date the software was first detected and what action
    should be taken if any.
    """

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False

    model_tag = None


    class Meta:
        ordering = [
            '-action',
            'software'
        ]

        verbose_name = 'IT Asset Software'

        verbose_name_plural = 'IT Asset Softwares'



    class Actions(models.IntegerChoices):
        INSTALL = 1, 'Install'
        REMOVE = 0, 'Remove'


    it_asset = models.ForeignKey(
        to = 'itam.ITAsset',
        blank = False,
        help_text = 'Device this software is on',
        on_delete = models.CASCADE,
        null = False,
        related_name = '+',
        verbose_name = 'Device'
    )

    software = models.ForeignKey(
        to = 'itam.Software',
        blank = False,
        help_text = 'Software Name',
        null = False,
        on_delete = models.PROTECT,
        verbose_name = 'Software'
    )

    action = models.IntegerField(
        blank = True,
        choices = Actions,
        help_text = 'Action to perform',
        null = True,
        verbose_name = 'Action',
    )

    version = models.ForeignKey(
        to = 'itam.SoftwareVersion',
        blank = True,
        help_text = 'Version to install',
        on_delete = models.PROTECT,
        null = True,
        verbose_name = 'Desired Version'
    )


    installedversion = models.ForeignKey(
        to = 'itam.SoftwareVersion',
        blank = True,
        help_text = 'Version that is installed',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'installedversion',
        verbose_name = 'Installed Version'
    )

    installed = models.DateTimeField(
        blank = True,
        help_text = 'Date detected as installed',
        null = True,
        verbose_name = 'Date Installed'
    )


    page_layout: dict = {
        "table": [
            "nbsp",
            "software",
            "category",
            "action_badge",
            "version",
            "installedversion",
            "installed",
            "nbsp"
        ]
    }


    @property
    def action_badge(self):

        from core.classes.badge import Badge

        text:str = 'Add'

        if self.action:

            text = self.get_action_display()

        return Badge(
            icon_name = f'action_{text.lower()}',
            icon_style = f'badge-icon-action-{text.lower()}',
            text = text,
            text_style = f'badge-text-action-{text.lower()}',
            url = '_self',
        )


    def get_tenant(self):
        return self.it_asset.organization


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        kwargs.update({
            'model_name': self.it_asset._meta.model_name,
            'model_id': self.it_asset.pk,
            'related_model_name': 'software',
        })

        return kwargs


    @property
    def parent_object(self):
        """ Fetch the parent object """

        return self.it_asset
