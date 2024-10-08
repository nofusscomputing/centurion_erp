from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from access.fields import *
from access.models import Team, TenancyObject

from itam.models.device import Device



class ClusterType(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Cluster Type"

        verbose_name_plural = "Cluster Types"


    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Cluster Type',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    slug = AutoSlugField()


    config = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Cluster Type Configuration that is applied to all clusters of this type',
        null = True,
        verbose_name = 'Configuration',
    )


    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    def __str__(self):

        return self.name



class Cluster(TenancyObject):


    class Meta:

        ordering = [
            'name',
        ]

        verbose_name = "Cluster"

        verbose_name_plural = "Clusters"


    id = models.AutoField(
        primary_key=True,
        unique=True,
        blank=False
    )

    parent_cluster = models.ForeignKey(
        'self',
        blank = True,
        default = None,
        help_text = 'Parent Cluster for this cluster',
        null = True,
        on_delete = models.CASCADE,
        verbose_name = 'Parent Cluster',
    )

    cluster_type = models.ForeignKey(
        ClusterType,
        blank = True,
        default = None,
        help_text = 'Type of Cluster',
        null = True,
        on_delete = models.CASCADE,
        verbose_name = 'Cluster Type',
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of the Cluster',
        max_length = 50,
        unique = False,
        verbose_name = 'Name',
    )

    slug = AutoSlugField()

    config = models.JSONField(
        blank = True,
        default = None,
        help_text = 'Cluster Configuration',
        null = True,
        verbose_name = 'Configuration',
    )

    nodes = models.ManyToManyField(
        Device,
        blank = True,
        default = None,
        help_text = 'Hosts for resource consumption that the cluster is deployed upon',
        related_name = 'cluster_node',
        verbose_name = 'Nodes',
    )

    devices = models.ManyToManyField(
        Device,
        blank = True,
        default = None,
        help_text = 'Devices that are deployed upon the cluster.',
        related_name = 'cluster_device',
        verbose_name = 'Devices',
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()


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

            rendered_config.update(
                self.config
            )



        return rendered_config


    def __str__(self):

        return self.name
