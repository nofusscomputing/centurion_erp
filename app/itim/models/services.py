import re

from django.db import models
from django.forms import ValidationError

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from itam.models.device import Device



class Port(
    CenturionModel
):

    model_tag = 'port'


    class Meta:

        ordering = [
            'number',
            'protocol',
        ]

        verbose_name = "Port"

        verbose_name_plural = "Ports"


    class Protocol(models.TextChoices):
        TCP = 'TCP', 'TCP'
        UDP = 'UDP', 'UDP'


    def validation_port_number(number: int):

        if number < 1 or number > 65535:

            raise ValidationError('A Valid port number is between 1-65535')

    number = models.IntegerField(
        blank = False,
        help_text = 'The port number',
        unique = False,
        validators = [ validation_port_number ],
        verbose_name = 'Port Number',
    )

    description = models.CharField(
        blank = True,
        help_text = 'Short description of port',
        max_length = 80,
        null = True,
        verbose_name = 'Description',
    )

    protocol = models.CharField(
        blank = False,
        choices=Protocol.choices,
        help_text = 'Layer 4 Network Protocol',
        max_length = 3,
        verbose_name = 'Protocol',
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
                        'display_name',
                        'description',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
            ]
        },
        {
            "name": "Services",
            "slug": "services",
            "sections": [
                {
                    "layout": "table",
                    "field": "services",
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
            "name": "Notes",
            "slug": "notes",
            "sections": []
        },
    ]


    table_fields: list = [
        'display_name',
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return str(self.protocol) + '/' + str(self.number)



class Service(
    CenturionModel
):

    model_tag = 'service'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Service"

        verbose_name_plural = "Services"

    def validate_config_key_variable(value):

        if not value:

            raise ValidationError('You must enter a config key.')

        valid_chars = search=re.compile(r'[^a-z_]').search

        if bool(valid_chars(value)):

            raise ValidationError('config key must only contain [a-z_].')

    is_template = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this service to be used as a template',
        verbose_name = 'Template',
    )

    template = models.ForeignKey(
        'self',
        blank = True,
        help_text = 'Template this service uses',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Template Name',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Service',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    device = models.ForeignKey(
        Device,
        blank = True,
        help_text = 'Device the service is assigned to',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Device',
    )

    cluster = models.ForeignKey(
        'Cluster',
        blank = True,
        help_text = 'Cluster the service is assigned to',
        null = True,
        on_delete = models.PROTECT,
        unique = False,
        verbose_name = 'Cluster',
    )

    config = models.JSONField(
        blank = True,
        help_text = 'Cluster Configuration',
        null = True,
        verbose_name = 'Configuration',
    )

    config_key_variable = models.CharField(
        blank = True,
        help_text = 'Key name to use when merging with cluster/device config.',
        max_length = 50,
        null = True,
        unique = False,
        validators = [ validate_config_key_variable ],
        verbose_name = 'Configuration Key',
    )

    port = models.ManyToManyField(
        Port,
        blank = True,
        help_text = 'Port the service is available on',
        verbose_name = 'Port',
    )

    dependent_service = models.ManyToManyField(
        'self',
        blank = True,
        help_text = 'Services that this service depends upon',
        related_name = 'dependentservice',
        symmetrical = False,
        verbose_name = 'Dependent Services',
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
                        'config_key_variable',
                        'template',
                        'is_template',
                    ],
                    "right": [
                        'model_notes',
                        'created',
                        'modified',
                    ]
                },
                {
                    "name": "cluster / Device",
                    "layout": "double",
                    "left": [
                        'cluster',
                    ],
                    "right": [
                        'device',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'config',
                    ]
                },
                {
                    "layout": "single",
                    "fields": [
                        'dependent_service'
                    ]
                },
                {
                    "layout": "single",
                    "name": "Ports",
                    "fields": [
                        'port'
                    ],
                }
            ]
        },
        {
            "name": "Rendered Config",
            "slug": "config_management",
            "sections": [
                {
                    "layout": "single",
                    "fields": [
                        "rendered_config",
                    ]
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
            "slug": "ticket",
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
        'deployed_to'
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return self.name


    def clean(self):

        if self.config_key_variable:

            self.config_key_variable = self.config_key_variable.lower()

        super().clean()


    @property
    def config_variables(self):

        config: dict = {}


        if self.template:

            if self.template.config:

                config.update(self.template.config)


        if self.config:

            config.update(self.config)

        return config
