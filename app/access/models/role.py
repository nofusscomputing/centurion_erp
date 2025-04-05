from django.contrib.auth.models import Permission
from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.tenancy import TenancyObject

from core.lib.feature_not_used import FeatureNotUsed



class Role(
    TenancyObject
):


    class Meta:

        ordering = [
            'organization',
            'name',
        ]

        verbose_name = 'Role'

        verbose_name_plural = 'Roles'


    id = models.AutoField(
        blank=False,
        help_text = 'Primary key of the entry',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    name = models.CharField(
        blank = False,
        help_text = 'Name of this role',
        max_length = 30,
        unique = False,
        verbose_name = 'Name'
    )

    permissions = models.ManyToManyField(
        Permission,
        blank = True,
        help_text = 'Permissions part of this role',
        related_name = 'roles',
        symmetrical = False,
        verbose_name = 'Permissions'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()

    is_global = None



    def __str__(self) -> str:
        
        return str( self.organization.name + ' ' + self.name )
