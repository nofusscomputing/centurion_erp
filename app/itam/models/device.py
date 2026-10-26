import json
import re

from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import (
    ValidationError
)
from django.db import models
from django.utils.timezone import now

from access.fields import AutoLastModifiedField

from centurion.helpers.merge_software import merge_software
from centurion.lib.decorators import depreciate

from core.classes.icon import Icon
from core.models.centurion import CenturionModel

from itam.models.device_models import DeviceModel
from itam.models.software import Software
from itam.models.operating_system import OperatingSystemVersion

from settings.models.app_settings import AppSettings



@depreciate(
    depreciated_in = '1.36.0',
    removed_in = '2.0',
    replacement = 'itam.ITAsset',
    skip_tests = True,
)
class Device(
    CenturionModel,
):    # pragma: no cover

    model_tag = 'device-'

    reserved_config_keys: list = [
        'software'
    ]

    class Meta:

        ordering = [
            'name',
            'organization'
        ]

        verbose_name = 'Device'

        verbose_name_plural = 'Devices'


    migrated_id = models.ForeignKey(
        to = 'itam.ITAsset',
        blank = True,
        help_text = 'IT Asset this device was migrated to.',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'IT Asset',
    )

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

    serial_number = models.CharField(
        blank = True,
        help_text = 'Serial number of the device.',
        max_length = 50,
        null = True,
        unique = True,
        verbose_name = 'Serial Number',

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

    device_model = models.ForeignKey(
        DeviceModel,
        blank = True,
        help_text = 'Model of the device.',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Model'
    )

    device_type = models.ForeignKey(
        to = 'itam.DeviceType',
        blank = True,
        help_text = 'Type of device.',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Type'
    )


    def validate_config_keys_not_reserved(self):

        if self:

            value: dict = self

            for invalid_key in Device.reserved_config_keys:

                if invalid_key in value.keys():
                    raise ValidationError(
                        message = f'json key "{invalid_key}" is a reserved configuration key'
                    )

    config = models.JSONField(
        blank = True,
        help_text = 'Configuration for this device',
        null = True,
        validators=[ validate_config_keys_not_reserved ],
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

    modified = AutoLastModifiedField()

    page_layout: dict = {
        "dataset":{
            "columns": [
                [
                    "name",
                    "device_model",
                    "device_type",
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
                            'device_type',
                            'device_model',
                            'name',
                            'serial_number',
                            'uuid',
                            'inventorydate',
                            'created',
                            'modified',
                        ],
                        "right": [
                            'model_notes',
                            'is_virtual',
                        ]
                    },
                    {
                        "layout": "table",
                        "name": "Operating System",
                        "field": "operating_system",
                    },
                    {
                        "layout": "table",
                        "name": "Dependent Services",
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
            "device_type",
            "organization",
            "created",
            "modified",
            "nbsp"
        ]
    }


    def clean_fields(self, exclude = None):

        if self.uuid is not None:

            self.uuid = str(self.uuid).lower()


        super().clean_fields(exclude = exclude)


    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
        ):
        """ Save Device Model

        After saving the device update the related items so that they are a part
        of the same organization as the device.
        """


        super().save(
            force_insert=False, force_update=False, using=None, update_fields=None
        )

        models_to_update =[ 
            DeviceSoftware,
            DeviceOperatingSystem
        ]

        for update_model in models_to_update:

            obj = update_model.objects.filter(
                device = self.id,
            )

            if obj.exists():

                obj.update(
                    organization = self.organization,
                )

        from config_management.models.groups import ConfigGroupHosts

        ConfigGroupHosts.objects.filter(
            host = self.id,
        ).delete()


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

            config_groups = ConfigGroupHosts.objects.filter(host=self.id).order_by('group')

            for group in config_groups:

                rendered_config = group.group.render_config()

                if rendered_config:

                    config.update(json.loads(rendered_config))

                    rendered_config: dict = json.loads(rendered_config)

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



    def migrate(self) -> None:

        new_model = apps.get_model(
            app_label = self._meta.app_label,
            model_name = 'itasset'
        )

        history_content_type = ContentType.objects.get_for_model(new_model())

        new_history_model = apps.get_model(
            app_label = new_model._meta.app_label,
            model_name = str(new_model().get_history_model_name()).lower()
        )

        new_notes_model = apps.get_model(
            app_label = new_model._meta.app_label,
            model_name = str(f'{new_model._meta.object_name}CenturionModelNote').lower()
        )

        new_ticket_model = apps.get_model(
            app_label = 'accounting',
            model_name = str(f'AssetBaseTicket').lower()
        )

        system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
            username = 'system'
        ).first()

        new_model.context[self._meta.model_name] = system_user


        created_object = ''

        current_model = self

        try:

            type(self).context['logger'].info(f"Begin migrating {self.pk} - {getattr(self, 'name', '')}.")

            device_model = None

            if getattr(self.device_model, 'migrated_id', None):
                device_model = self.device_model.migrated_id


            created_object = new_model.objects.create(
                organization = self.organization,
                name = self.name,
                uuid = self.uuid,
                serial_number = self.serial_number,
                device_model = device_model,
                config = self.config,
                inventorydate = self.inventorydate,
                is_virtual = self.is_virtual,
                created = self.created,
                modified = self.modified,

            )


            type(self).context['logger'].info(f'Migrated {self.pk} to {created_object.pk}.')

            tickets_model = apps.get_model(
                app_label = current_model._meta.app_label,
                model_name = str(f'{current_model._meta.object_name}Ticket').lower()
            )

            type(self).context['logger'].info(f'Begin migrate model tickets for {self.pk}.')

            for ticket_entry in tickets_model.objects.filter(
                model = current_model
            ):

                new_ticket_model.objects.create(
                    organization = ticket_entry.organization,
                    created = ticket_entry.created,
                    ticket = ticket_entry.ticket,
                    modified = ticket_entry.modified,

                    model = created_object,

                )

                type(self).context['logger'].info(f'Migrate model ticket {ticket_entry.pk} to {new_notes_model.pk}.')


            notes_model = apps.get_model(
                app_label = current_model._meta.app_label,
                model_name = str(f'{current_model._meta.object_name}CenturionModelNote').lower()
            )

            type(self).context['logger'].info(f'Begin migrate notes for {self.pk}.')

            for notes_entry in notes_model.objects.filter(
                model_id = current_model.pk
            ):

                new_notes_model.objects.create(
                    body = notes_entry.body,
                    created_by = notes_entry.created_by,
                    modified_by = notes_entry.modified_by,

                    model = created_object,

                    organization = notes_entry.organization,
                    created = notes_entry.created,
                    modified = notes_entry.modified,


                )

                type(self).context['logger'].info(f'Migrate note {notes_entry.pk} to {new_notes_model.pk}.')


            type(self).context['logger'].info(f'Begin migrate audit entries for {self.pk}.')

            history_model = apps.get_model(
                app_label = current_model._meta.app_label,
                model_name = str(current_model.get_history_model_name()).lower()
            )

            for audit_entry in history_model.objects.filter(
                model_id = current_model.pk
            ):

                new_audit_entry = new_history_model.objects.create(
                    content_type = history_content_type,

                    model = created_object,

                    before = audit_entry.before,
                    after = audit_entry.after,
                    action = audit_entry.action,
                    user = audit_entry.user,
                    organization = audit_entry.organization,
                    created = audit_entry.created

                )

                type(self).context['logger'].info(f'Migrate audit_entry {audit_entry.pk} to {new_audit_entry.id}.')


            # current_model.configgrouphosts_set.all()
            for field in current_model.configgrouphosts_set.all():

                # field.hosts.add( created_object )
                created_object.configgrouphosts_set.add( field )

                # field.save()

            # current_model.configgroups_set.all()
            for field in current_model.configgroups_set.all():

                # field.hosts.add( created_object )
                created_object.configgroups_set.add( field )

                # field.save()

            # current_model.cluster_device.all()
            for field in current_model.cluster_device.all():

                # field.devices.add( created_object )
                created_object.cluster_device.add( field )

                # field.save()

            # current_model.cluster_node.all()
            for field in current_model.cluster_node.all():

                # field.nodes.add( created_object )
                created_object.cluster_node.add( field )

                # field.save()

            # current_model.service_set.all()
            for field in current_model.service_set.all():

                # field.device.add( created_object )
                created_object.service_set.add( field )

                # field.save()


            kb_articles = apps.get_model(
                app_label = 'assistance',
                model_name = 'modelknowledgebasearticle'
            )

            for article in kb_articles.objects.filter(
                model = f'{self._meta.app_label}.{self._meta.model_name}',
                model_pk = self.id
            ):

                article.model = f'{created_object._meta.app_label}.{created_object._meta.model_name}'

                article.model_pk = created_object.id

                article.save()


            self.migrated_id = created_object
            self.save()


        except Exception as exc:
            type(self).context['logger'].exception(exc)


            if hasattr( created_object, 'pk'):    # Remove migrated object

                tickets_model = apps.get_model(
                    app_label = 'accounting',
                    model_name = str(f'AssetBaseTicket').lower()
                )

                type(self).context['logger'].info(f'Begin migrate model tickets for {self.pk}.')

                for ticket_entry in tickets_model.objects.filter(
                    model = created_object
                ):

                    type(self).context['logger'].info(f'Reverting model ticket {ticket_entry.pk} to {new_ticket_model.pk}.')

                    ticket_entry.delete()


                kb_articles = apps.get_model(
                    app_label = 'assistance',
                    model_name = 'modelknowledgebasearticle'
                )

                for article in kb_articles.objects.filter(
                    model = f'{created_object._meta.app_label}.{created_object._meta.model_name}',
                    model_pk = created_object.id
                ):

                    article.model = f'{self._meta.app_label}.{self._meta.model_name}'

                    article.model_pk = self.id

                    article.save()



                type(self).context['logger'].notice('Begin reverting created notes.')

                for note in new_notes_model.objects.filter(
                    model = created_object
                ):

                    type(self).context['logger'].notice(f'Reverting note {note.pk}.')

                    note.delete()


                type(self).context['logger'].notice('Begin reverting created audit entries.')

                for history_model in new_history_model.objects.filter(
                    model = created_object
                ):

                    type(self).context['logger'].notice(f'Reverting note {history_model.pk}.')

                    history_model.delete()


                type(self).context['logger'].notice(f'Revert created model {created_object.pk}.')

                created_object.delete()


        del new_model.context[self._meta.model_name]

        type(self).context['logger'].info(f"Completed migration for {self.pk} - {self.name}.")




@depreciate(
    depreciated_in = '1.36.0',
    removed_in = '2.0',
    skip_tests = True,
)
class DeviceSoftware(
    CenturionModel,
):    # pragma: no cover
    """ A way for the device owner to configure software to install/remove """

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False


    class Meta:
        ordering = [
            '-action',
            'software'
        ]

        verbose_name = 'Device Software'

        verbose_name_plural = 'Device Softwares'



    class Actions(models.IntegerChoices):
        INSTALL = 1, 'Install'
        REMOVE = 0, 'Remove'


    device = models.ForeignKey(
        Device,
        blank = False,
        help_text = 'Device this software is on',
        on_delete = models.CASCADE,
        null = False,
        verbose_name = 'Device'
    )

    software = models.ForeignKey(
        Software,
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

    modified = AutoLastModifiedField()


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


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        kwargs.update({
            'device_id': self.device.id,
        })

        return kwargs


    @property
    def parent_object(self):
        """ Fetch the parent object """

        return self.device



@depreciate(
    depreciated_in = '1.36.0',
    removed_in = '2.0',
    skip_tests = True,
)
class DeviceOperatingSystem(
    CenturionModel,
):    # pragma: no cover

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False

    class Meta:

        ordering = [
            'device',
        ]

        verbose_name = 'Device Operating System'

        verbose_name_plural = 'Device Operating Systems'

    model_notes = None

    device = models.OneToOneField(
        Device,
        blank = False,
        help_text = 'Device for the Operating System',
        on_delete = models.CASCADE,
        null = False,
        verbose_name = 'Device',
        unique = True
    )

    operating_system_version = models.ForeignKey(
        OperatingSystemVersion,
        blank = False,
        help_text = 'Operating system version',
        null = False,
        on_delete = models.PROTECT,
        verbose_name = 'Operating System/Version',

    )

    version = models.CharField(
        blank = False,
        help_text = 'Version detected as installed',
        max_length = 15,
        null = False,
        verbose_name = 'Installed Version',
    )

    installdate = models.DateTimeField(
        blank = True,
        help_text = 'Date and time detected as installed',
        null = True,
        verbose_name = 'Install Date',
    )

    modified = AutoLastModifiedField()

    page_layout: dict = {
        "detail": [
            {
                "name": "Details",
                "slug": "details",
                "sections": [
                    {
                        "layout": "single",
                        "fields": [
                            'operating_system_version',
                            'version',
                            'installdate'
                        ],
                    }
                ]
            }
        ],
        "table": [
            'device',
            'operating_system_version',
            'version',
            'installdate',
        ]
    }


    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        kwargs.update({
            'device_id': self.device.id,
        })

        return kwargs


    @property
    def parent_object(self):
        """ Fetch the parent object """

        return self.device
