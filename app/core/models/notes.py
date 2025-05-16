import django

from django.conf import settings
from django.db import models

from rest_framework.reverse import reverse

from access.fields import *
from access.models.tenancy import TenancyObject

from config_management.models.groups import ConfigGroups

from itam.models.device import Device
from itam.models.software import Software
from itam.models.operating_system import OperatingSystem

from itim.models.services import Service

User = django.contrib.auth.get_user_model()



class NotesCommonFields(TenancyObject, models.Model):

    class Meta:
        abstract = True

    id = models.AutoField(
        blank=False,
        help_text = 'ID of this note',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    created = AutoCreatedField()

    modified = AutoLastModifiedField()



class Notes(NotesCommonFields):
    """ Notes that can be left against a model 

    Currently supported models are:
        - Device
        - Operating System
        - Software
    """

    class Meta:

        ordering = [
            '-created'
        ]

        verbose_name = 'Note'

        verbose_name_plural = 'Notes'



    note = models.TextField(
        blank = False,
        help_text = 'The tid bit you wish to add',
        null = False,
        verbose_name = 'Note',
    )


    usercreated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank= True,
        default = None,
        help_text = 'User whom added Note',
        null = True,
        on_delete=models.DO_NOTHING,
        related_name = 'usercreated',
        verbose_name = 'Added By',
    )

    usermodified = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank= True,
        default = None,
        help_text = 'User whom modified the note',
        null = True,
        on_delete=models.DO_NOTHING,
        related_name = 'usermodified',
        verbose_name = 'Edited By',
    )

    config_group = models.ForeignKey(
        ConfigGroups,
        blank= True,
        default = None,
        help_text = 'Config group this note belongs to',
        null = True,
        on_delete=models.CASCADE,
        related_name = '+',
        verbose_name = 'Config Group'
    )

    device = models.ForeignKey(
        Device,
        blank= True,
        default = None,
        help_text = 'Device this note belongs to',
        null = True,
        on_delete=models.CASCADE,
        related_name = '+',
        verbose_name = 'Device'
    )

    service = models.ForeignKey(
        Service,
        blank= True,
        default = None,
        help_text = 'Service this note belongs to',
        null = True,
        on_delete=models.CASCADE,
        related_name = '+',
        verbose_name = 'Service'
    )

    software = models.ForeignKey(
        Software,
        blank= True,
        default = None,
        help_text = 'Software this note belongs to',
        null = True,
        on_delete=models.CASCADE,
        related_name = '+',
        verbose_name = 'Software'
    )

    operatingsystem = models.ForeignKey(
        OperatingSystem,
        blank= True,
        default = None,
        help_text = 'Operating system this note belongs to',
        null = True,
        on_delete=models.CASCADE,
        related_name = '+',
        verbose_name = 'Operating System'
    )

    # this model is not intended to have its own viewable page as
    # it's a sub model
    page_layout: dict = []

    # This model is not expected to be viewable in a table
    # as it's a sub-model
    table_fields: list = []

    def __str__(self):

        return 'Note ' + str(self.id)


    def get_url( self, request = None ) -> str:

        kwargs = self.get_url_kwargs()

        if self.config_group:

            item = 'config_group'

            item_id = self.config_group.id
        
        elif self.device:

            item = 'device'

            item_id = self.device.id

        elif self.service:

            item = 'service'

            item_id = self.service.id

        elif self.software:

            item = 'software'

            item_id = self.software.id

        elif self.operatingsystem:

            item = 'operating_system'

            item_id = self.operatingsystem.id

        kwargs.update({
            str(item + '_id'): item_id
        })


        if request:

            return reverse(f"v2:_api_v2_{item}_notes-detail", request=request, kwargs = kwargs )

        return reverse(f"v2:_api_v2_{item}_notes-detail", kwargs = kwargs )
