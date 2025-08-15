import json

from django.db import models

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel

from itam.models.device import Device



class ClusterType(
    CenturionModel
):

    model_tag = 'cluster_type'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Cluster Type"

        verbose_name_plural = "Cluster Types"


    name = models.CharField(
        blank = False,
        help_text = 'Name of the Cluster Type',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    config = models.JSONField(
        blank = True,
        help_text = 'Cluster Type Configuration that is applied to all clusters of this type',
        null = True,
        verbose_name = 'Configuration',
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
                        'modified',
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
        'organization',
        'created',
        'modified'
    ]


    def __str__(self):

        return self.name



class Cluster(
    CenturionModel
):

    model_tag = 'cluster'


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Cluster"

        verbose_name_plural = "Clusters"


    parent_cluster = models.ForeignKey(
        'self',
        blank = True,
        help_text = 'Parent Cluster for this cluster',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Parent Cluster',
    )

    cluster_type = models.ForeignKey(
        ClusterType,
        blank = True,
        help_text = 'Type of Cluster',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Cluster Type',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Cluster',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    config = models.JSONField(
        blank = True,
        help_text = 'Cluster Configuration',
        null = True,
        verbose_name = 'Configuration',
    )

    nodes = models.ManyToManyField(
        Device,
        blank = True,
        help_text = 'Hosts for resource consumption that the cluster is deployed upon',
        related_name = 'cluster_node',
        verbose_name = 'Nodes',
    )

    devices = models.ManyToManyField(
        Device,
        blank = True,
        help_text = 'Devices that are deployed upon the cluster.',
        related_name = 'cluster_device',
        verbose_name = 'Devices',
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
                        'parent_cluster',
                        'cluster_type',
                        'name',
                    ],
                    "right": [
                        'model_notes',
                        'resources',
                        'created',
                        'modified',
                    ]
                },
                {
                    "layout": "double",
                    "name": "Nodes / Devices",
                    "left": [
                        'nodes',
                    ],
                    "right": [
                        'devices',
                    ]
                },
                {
                    "layout": "table",
                    "name": "Services",
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
        'parent_cluster',
        'cluster_type',
        'organization',
        'created',
        'modified'
    ]


    @property
    def rendered_config(self):

        from itim.models.services import Service

        rendered_config: dict = {}

        if self.cluster_type:

            if self.cluster_type.config:

                rendered_config.update(
                    self.cluster_type.config
                )


        for service in Service.objects.filter(cluster = self.pk):

            if service.config_variables:

                rendered_config.update( service.config_variables )


        if self.config:

            if isinstance(self.config, str):
                self.config = json.loads(self.config)
                self.save()

            rendered_config.update(
                self.config
            )



        return rendered_config


    def __str__(self):

        return self.name
