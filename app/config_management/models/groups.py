import re

from django.core.exceptions import (
    ValidationError
)
from django.db import models

from access.fields import AutoLastModifiedField

from centurion.helpers.merge_software import merge_software

from core.models.centurion import CenturionModel

from itam.models.device import Device, DeviceSoftware
from itam.models.software import Software, SoftwareVersion



class ConfigGroups(
    CenturionModel,
):

    model_tag = 'config_group'

    class Meta:

        ordering = [
            'name'
        ]

        verbose_name = 'Config Group'

        verbose_name_plural = 'Config Groups'


    reserved_config_keys: list = [
        'software'
    ]


    def validate_config_keys_not_reserved(self):

        if self is not None:

            value: dict = self

            for invalid_key in ConfigGroups.reserved_config_keys:

                if invalid_key in value.keys():

                    raise ValidationError(
                        message = f'json key "{invalid_key}" is a reserved configuration key'
                    )


    parent = models.ForeignKey(
        'self',
        blank= True,
        help_text = 'Parent of this Group',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Parent Group'
    )


    name = models.CharField(
        blank = False,
        help_text = 'Name of this Group',
        max_length = 50,
        unique = False,
        verbose_name = 'Name'
    )


    config = models.JSONField(
        blank = True,
        help_text = 'Configuration for this Group',
        null = True,
        validators=[ validate_config_keys_not_reserved ],
        verbose_name = 'Configuration'
    )

    hosts = models.ManyToManyField(
        to = Device,
        blank = True,
        help_text = 'Hosts that are part of this group',
        verbose_name = 'Hosts'
    )

    modified = AutoLastModifiedField()


    page_layout: dict = [
        {
            "name": "Details",
            "slug": "details",
            "sections": [
                {
                    "layout": "double",
                    "left": [
                        'organization',
                        'name',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified'
                    ]
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
            "name": "Child Groups",
            "slug": "child_groups",
            "sections": [
                {
                    "layout": "table",
                    "field": "child_groups",
                }
            ]
        },
        {
            "name": "Hosts",
            "slug": "hosts",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        "hosts"
                    ],
                }
            ]
        },
        {
            "name": "Software",
            "slug": "software",
            "sections": [
                {
                    "layout": "table",
                    "field": "group_software",
                }
            ]
        },
        {
            "name": "Configuration",
            "slug": "configuration",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        "rendered_config"
                    ],
                }
            ]
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
            "name": "Tickets",
            "slug": "tickets",
            "sections": [
                {
                    "layout": "table",
                    "field": "tickets",
                }
            ]
        },
        {
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]


    table_fields: list = [
        'name',
        'child_count',
        'organization',
    ]



    def clean_fields(self, exclude = None):

        if self.config:

            self.config = self.config_keys_ansible_variable(self.config)

        if self.parent:
            self.organization = ConfigGroups.objects.get(id=self.parent.id).organization

        if self.pk:

            obj = ConfigGroups.objects.get(
                id = self.id,
            )

            # Prevent organization change. ToDo: add feature so that config can change organizations
            self.organization = obj.organization

        if self.parent is not None:

            if self.pk == self.parent.pk:

                raise ValidationError('Can not set self as parent')


        super().clean_fields(exclude = exclude)



    def config_keys_ansible_variable(self, value: dict):

        clean_value = {}

        for key, value in value.items():

            key: str = str(key).lower()

            key = re.sub('\s|\.|\-', '_', key) # make an '_' char

            if type(value) is dict:

                clean_value[key] = self.config_keys_ansible_variable(value)

            else:

                clean_value[key] = value

        return clean_value


    def count_children(self) -> int:
        """ Count all child groups recursively

        Returns:
            int: Total count of ALL child-groups
        """

        count = 0

        children = ConfigGroups.objects.filter(parent=self.pk)

        for child in children.all():

            count += 1

            count += child.count_children()

        return count



    def render_config(self):

        config: dict = dict()

        if self.parent:

            config.update(ConfigGroups.objects.get(id=self.parent.id).render_config())

        if self.config:

            config.update(self.config)

        softwares = ConfigGroupSoftware.objects.filter(config_group=self.id)

        software_actions = {
            "software": []
        }

        for software in softwares:

            if software.action:

                if int(software.action) == 1:

                    state = 'present'

                elif int(software.action) == 0:

                    state = 'absent'

                software_action = {
                    "name": software.software.slug,
                    "state": state
                }


                if software.version:
                    software_action['version'] = software.version.name

                software_actions['software'] = software_actions['software'] + [ software_action ]

        if len(software_actions['software']) > 0:
            # don't add empty software as it prevents parent software from being added

            if 'software' not in config.keys():

                config['software'] = []

            config['software'] = merge_software(config['software'], software_actions['software'])

        return config




    def __str__(self):

        if self.parent:

            return f'{self.parent} > {self.name}'

        return self.name



class ConfigGroupHosts(
    CenturionModel,
):


    def validate_host_no_parent_group(self):
        """ Ensure that the host is not within any parent group

        Raises:
            ValidationError: host exists within group chain
        """

        if False:
            raise ValidationError(
                message = f'host {self} ' \
                    'is already a member of this chain as it;s a member of group ""'
            )


    host = models.ForeignKey(
        Device,
        blank = False,
        help_text = 'Host that will be apart of this config group',
        on_delete = models.PROTECT,
        null = False,
        validators = [ validate_host_no_parent_group ],
        verbose_name = 'Host',
    )


    group = models.ForeignKey(
        ConfigGroups,
        blank= False,
        help_text = 'Group that this host is part of',
        on_delete = models.PROTECT,
        null = False,
        verbose_name = 'Group',
    )

    modified = AutoLastModifiedField()


    @property
    def parent_object(self):
        """ Fetch the parent object """

        return self.group


    page_layout: list = []
    table_fields: list = []



class ConfigGroupSoftware(
    CenturionModel,
):
    """ A way to configure software to install/remove per config group """

    class Meta:

        ordering = [
            '-action',
            'software'
        ]

        verbose_name = 'Config Group Software'

        verbose_name_plural = 'Config Group Softwares'


    config_group = models.ForeignKey(
        ConfigGroups,
        blank = False,
        help_text = 'Config group this softwre will be linked to',
        null = False,
        on_delete = models.PROTECT,
        verbose_name = 'Config Group'
    )


    software = models.ForeignKey(
        Software,
        blank = False,
        help_text = 'Software to add to this config Group',
        null = False,
        on_delete = models.PROTECT,
        verbose_name = 'Software'
    )


    action = models.IntegerField(
        blank = True,
        choices = DeviceSoftware.Actions,
        help_text = 'ACtion to perform with this software',
        null = True,
        verbose_name = 'Action'
    )

    version = models.ForeignKey(
        SoftwareVersion,
        blank = True,
        help_text = 'Software Version for this config group',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Verrsion',
    )

    modified = AutoLastModifiedField()

    # This model is not intended to be viewable on it's own page
    # as it's a sub model for config groups
    page_layout: dict = []


    table_fields: list = [
        'software',
        'category',
        'action',
        'version'
    ]


    def get_url_kwargs(self, many = False) -> dict:
        
        kwargs = super().get_url_kwargs(many = many)

        kwargs.update({
            'config_group_id': self.config_group.id
        })
        return kwargs


    @property
    def parent_object(self):
        """ Fetch the parent object """

        return self.config_group
