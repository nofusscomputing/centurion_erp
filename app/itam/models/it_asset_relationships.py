from django.db import models

from core.mixins.centurion import Centurion


class ITAssetRelationships(Centurion):
    """IT Asset Children

    This model is a custom m2m table.
    
    It's used by `DeviceType` to denote what other devices can connect to it.
    Then when the user creates a device each of the relationships are added to
    the device as empty "slots."

    Then Device will use this for linking the children devices.
    """

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False



    class Meta:

        ordering = [
            'child_asset_model__device_type__name',
            'child__name',
            'name',
        ]

        verbose_name = 'Device Connection'

        verbose_name_plural = 'Device Connections'



    name = models.CharField(
        blank = False,
        help_text = 'Name used for templating the child assets name.',
        max_length = 100
    )

    asset_type = models.ForeignKey(
        to = 'itam.DeviceType',
        blank = True,
        help_text = 'Type of asset.',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Type'
    )

    parent_asset_model = models.ForeignKey(
        to = 'itam.ITAssetModel',
        blank = False,
        help_text = 'Parent Asset Model.',
        on_delete = models.CASCADE,
        related_name = '+'
    )

    parent = models.ForeignKey(
        to = 'itam.ITAsset',
        blank = True,
        null = True,
        on_delete = models.CASCADE,
        related_name = '+'
    )

    child = models.ForeignKey(
        to = 'itam.ITAsset',
        blank = True,
        null = True,
        on_delete = models.CASCADE,
        related_name = '+'
    )

    child_asset_model = models.ForeignKey(
        to = 'itam.ITAssetModel',
        blank = True,
        null = True,
        help_text = 'Child Asset model to limit this child to.',
        on_delete = models.CASCADE,
        related_name = '+'
    )

    page_layout: dict = {
        "table": [
            'name',
            'parent_asset_model',
            'parent',
            'asset_type',
            'child_asset_model',
            'child',
            '-action_delete-',
        ]
    }



    def get_url_kwargs(self, many=False) -> dict:
        kwargs = super().get_url_kwargs(many)

        kwargs['model_name'] = str( self.parent_asset_model._meta.model_name )
        kwargs['model_id'] = str( self.parent_asset_model.pk )
        kwargs['related_model_name'] = 'connections'


        return kwargs
