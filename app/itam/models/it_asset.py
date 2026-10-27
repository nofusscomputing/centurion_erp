import json
import re

from datetime import timedelta

from django.core.exceptions import (
    ValidationError
)
from django.db import models
from django.utils.timezone import now

from centurion.helpers.merge_software import merge_software

from core.classes.icon import Icon

from .device import DeviceSoftware

from .software import Software

from .itam_asset_base import ITAMAssetBase



class ITAsset(
    ITAMAssetBase,
):


    model_tag = 'device'

    reserved_config_keys: list = [
        'software'
    ]

    class Meta:

        ordering = [
            'name',
            'organization'
        ]

        verbose_name = 'IT Asset'

        verbose_name_plural = 'IT Asset'


    def validate_hostname_format(self):

        pattern = r'^[a-z]{1}[a-z|0-9|\-]+[a-z|0-9]{1}$'

        if not re.match(pattern, str(self).lower()):

            raise ValidationError(
                message = '[RFC1035 2.3.1] A hostname must start with a letter,' \
                    'end with a letter or digit, and have as interior characters only letters,' \
                        ' digits, and hyphen.',
                code = 'invalid_hostname'
            )

    name = models.CharField(
        blank = False,
        help_text = 'Hostname of this device',
        max_length = 50,
        unique = True,
        validators = [ validate_hostname_format ],
        verbose_name = 'Name'
    )


    def validate_uuid_format(self):

        pattern = r'[0-9|a-f|A-F]{8}\-[0-9|a-f|A-F]{4}\-[0-9|a-f|A-F]{4}\-[0-9|a-f|A-F]{4}\-[0-9|a-f|A-F]{12}'

        if not re.match(pattern, str(self)):

            raise ValidationError(
                message = f'UUID must be formated to match regex {str(pattern)}',
                code = 'invalid_uuid'
            )

    uuid = models.UUIDField(
        blank = True,
        help_text = 'System GUID/UUID.',
        max_length = 50,
        null = True,
        unique = True,
        validators = [ validate_uuid_format ],
        verbose_name = 'UUID'
    )

    imei = models.CharField(
        blank = True,
        help_text = 'IMEI of this device',
        max_length = 50,
        null = True,
        unique = True,
        verbose_name = 'IMEI'
    )


    def validate_mac_address_format(self):

        pattern = r'^([0-9|A-F]{2}:){5}[0-9|A-F]{2}$'

        if not re.match(pattern, str(self)):

            raise ValidationError(
                message = f'UUID must be formated to match regex {str(pattern)}',
                code = 'invalid_mac_address'
            )

    mac_address = models.CharField(
        blank = True,
        help_text = 'MAC Address of this device',
        max_length = 50,
        null = True,
        unique = True,
        validators = [ validate_mac_address_format ],
        verbose_name = 'MAC Address'
    )

    puk = models.CharField(
        blank = True,
        help_text = 'PUK of this device',
        max_length = 50,
        null = True,
        unique = True,
        verbose_name = 'PUK'
    )

    puk_pin = models.CharField(
        blank = True,
        help_text = 'PUK PIN of this device',
        max_length = 50,
        null = True,
        unique = True,
        verbose_name = 'PUK PIN'
    )

    device_model = models.ForeignKey(
        to = 'itam.ITAssetModel',
        blank = True,
        help_text = 'Model of this device.',
        null = True,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Model'
    )

    def validate_config_keys_not_reserved(self):

        if self:

            value: dict = self

            for invalid_key in ITAsset.reserved_config_keys:

                if invalid_key in value.keys():
                    raise ValidationError(
                        message = f'json key "{invalid_key}" is a reserved configuration key'
                    )

    config = models.JSONField(
        blank = True,
        help_text = 'Configuration for this device',
        null = True,
        validators = [ validate_config_keys_not_reserved ],
        verbose_name = 'Host Configuration',
    )

    inventorydate = models.DateTimeField(
        blank = True,
        help_text = 'Date and time of the last inventory',
        null = True,
        verbose_name = 'Last Inventory Date',
    )

    is_virtual = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Is this device a virtual machine',
        null = False,
        verbose_name = 'Is Virtual',
    )

    operating_system = models.ManyToManyField(
        to = 'itam.OperatingSystemVersion',
        symmetrical = True,
        through = 'itam.ITAssetOperatingSystem',
        through_fields = ('it_asset', 'operating_system_version'),
    )

    page_layout: dict = {
        "dataset":{
            "columns": [
                [
                    "name",
                    "asset_type",
                    "device_model",
                    'status_icon',
                ],
                [
                    "organization",
                    "created",
                    "modified",
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
                            'device_model',
                            'name',
                            "asset_type",
                            'serial_number',
                            'uuid',
                            'inventorydate',
                            'created',
                            'modified',
                        ],
                        "right": [
                            'model_notes',
                            'is_virtual',
                            'imei',
                            'mac_address',
                            'puk',
                            'puk_pin',
                        ]
                    },
                    {
                        "layout": "table",
                        "name": "Operating System",
                        "field": "operating_system",
                    },
                    {
                        "layout": "table",
                        "name": "Deployed Services",
                        "field": "service",
                    },
                    {
                        "layout": "single",
                        "fields": [
                            'config',
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
                "name": "Software",
                "slug": "software",
                "sections": [
                    {
                        "layout": "table",
                        "field": "software",
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
            },
            {
                "name": "Config Management",
                "slug": "config_management",
                "sections": [
                    {
                        "layout": "single",
                        "fields": [
                            "rendered_config",
                        ]
                    }
                ]
            }
        ],
        "table": [
            'status_icon',
            "name",
            "device_model",
            "organization",
            "created",
            "modified",
            "nbsp"
        ]
    }


    def clean_fields_asset_model(self):

        for mandatory_field in [
            'imei',
            'mac_address',
            'puk',
            'puk_pin',
            'serial_number',
        ]:
        
            if self.device_model:

                if getattr(self.device_model, mandatory_field):

                    if getattr(self, mandatory_field) in [None, '']:

                        raise ValidationError(
                            message = {
                                mandatory_field: f'field {mandatory_field} has been set as mandatory and must be populated.'},
                            code = 'required'
                        )



    def clean_fields(self, exclude = None) -> None:

        # if virtual set the asset_type = 'Intangible'

        self.clean_fields_asset_model()

        if self.uuid is not None:

            self.uuid = str(self.uuid).lower()


        super().clean_fields(exclude = exclude)


    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
        ) -> None:
        """ Save Device Model

        After saving the device update the related items so that they are a part
        of the same organization as the device.
        """

        created = False
        if self.pk is None and getattr(self, 'device_model', None):

            created = True


        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

        if created:

            self.device_model.create_asset_connections(parent_asset = self)

        # models_to_update =[ 
        #     DeviceSoftware,
        #     DeviceOperatingSystem
        # ]

        # for update_model in models_to_update:

        #     obj = update_model.objects.filter(
        #         device = self.id,
        #     )

        #     if obj.exists():

        #         obj.update(
        #             organization = self.organization,
        #         )

        # from config_management.models.groups import ConfigGroupHosts

        # ConfigGroupHosts.objects.filter(
        #     host = self.id,
        # ).delete()


    def __str__(self):

        return self.name



    @property
    def status_icon(self) -> list([Icon]):

        icons: list(Icon) = []

        icons += [
            Icon(
                name = f'device_status_{self.status.lower()}',
                style = f'icon-device-status-{self.status.lower()}'
            )
        ]

        return icons


    @property
    def status(self) -> str:
        """ Fetch Device status

        Returns:
            str: Current status of the item
        """

        if self.inventorydate:

            check_date = self.inventorydate

        else:

            check_date = now() + timedelta(days=99)

        one = (now() - check_date).days

        status: str = 'UNK'

        if (now() - check_date).days >= 0 and (now() - check_date).days <= 1:

            status = 'OK'

        elif (now() - check_date).days >= 2 and (now() - check_date).days < 3:

            status = 'WARN'

        elif (now() - check_date).days >= 3:

            status = 'BAD'

        return status


    @property
    def get_configuration(self):

        softwares = DeviceSoftware.objects.filter(device=self.id)

        config = {
            "software": []
        }

        host_software = []
        group_software = []

        for software in softwares:

            if software.action:
            
                if int(software.action) == 1:

                    state = 'present'

                elif int(software.action) == 0:

                    state = 'absent'

                software_action = {
                    "name": str(Software),
                    "state": state
                }


                if software.version:
                    software_action['version'] = software.version.name

                host_software += [ software_action ]

        config: dict = config

        from config_management.models.groups import ConfigGroupHosts

        if self.id:

            for group in self.configgroups_set.all():

                rendered_config = group.render_config()

                if rendered_config:

                    config.update(rendered_config)

                    if 'software' in rendered_config.keys():
                        
                        group_software = group_software + rendered_config['software']

            config['software'] = merge_software(group_software, host_software)

            if self.config:

                config.update(self.config)

            from itim.models.services import Service
            services = Service.objects.filter(
                device = self.pk
            )

            for service in services:

                if service.config_variables:

                    service_config:dict = {
                        service.config_key_variable: service.config_variables
                    }

                    config.update(service_config)

        return config
