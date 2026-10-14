from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel



class ITAssetModel(CenturionModel):

    model_tag = 'itam_asset_type'


    class Meta:

        ordering = [
            'manufacturer',
            'name'
        ]

        verbose_name = 'IT Asset Model'

        verbose_name_plural = 'IT Asset Models'



    name = models.CharField(
        blank = False,
        help_text = 'Model name manufacturer provided.',
        max_length = 50,
        null = True,
        unique = True,
        verbose_name = 'Model Name'
    )

    device_type = models.ForeignKey(
        to = 'itam.DeviceType',
        blank = True,
        help_text = 'Type of device.',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Type'
    )

    manufacturer = models.ForeignKey(
        to = 'access.Company',
        blank = True,
        help_text = 'Who is the Manufacturer',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+'
    )

    imei = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Make "IMEI" a mandatory field',
        null = False,
        verbose_name = 'IMEI',
    )

    mac_address = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Make "MAC Address" a mandatory field',
        null = False,
        verbose_name = 'MAC Address',
    )

    puk = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Make "PUK" a mandatory field',
        null = False,
        verbose_name = 'PUK',
    )

    puk_pin = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Make "PUK Pin" a mandatory field',
        null = False,
        verbose_name = 'PUK Pin',
    )

    serial_number = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Make "Serial Number" a mandatory field',
        null = False,
        verbose_name = 'Serial Number',
    )

    modified = AutoLastModifiedField()


    page_layout: dict = {
        "dataset": {
            "columns": [
                [
                    {
                        "field": "display_name",
                        "type": "link",
                        "key": "_self"
                    },
                    'device_type',
                    'organization',
                    'created',
                    'modified'
                ]
            ]
        },
        "detail": [
            {
                "name": "Details",
                "slug": "details",
                "sections": [
                    {
                        "layout": "double",
                        "left": [
                            'organization',
                            'manufacturer',
                            'name',
                            'device_type',
                        ],
                        "right": [
                            'model_notes',
                            'created',
                            'modified',
                        ]
                    },
                    {
                        "name": "Mandatory Fields",
                        "layout": "double",
                        "left": [
                            'imei',
                            'puk',
                            'serial_number',
                        ],
                        "right": [
                            'mac_address',
                            'puk_pin',
                        ]
                    }
                ]
            },
            {
                "name": "Connections",
                "slug": "connections",
                "sections": [
                    {
                        "layout": "table",
                        "field": "connections",
                    }
                ]
            },
            {
                "name": "Tickets",
                "slug": "tickets",
                "sections": [
                    {
                        "layout": "table",
                        "field": "tickets",
                    }
                ],
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
            }
        ],
        "table": [
            {
                "field": "display_name",
                "type": "link",
                "key": "_self"
            },
            'organization',
            'created',
            'modified'
        ]
    }

    def __str__(self) -> str:

        return self.manufacturer.name + ' ' + self.name
