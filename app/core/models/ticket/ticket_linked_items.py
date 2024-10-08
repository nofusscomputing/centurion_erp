from django.db import models

from .ticket_enum_values import TicketValues

from access.models import TenancyObject

from core.middleware.get_request import get_request
from core.models.ticket.ticket import Ticket



class TicketLinkedItem(TenancyObject):

    class Meta:

        ordering = [
            'id'
        ]

        verbose_name = 'Ticket Linked Item'

        verbose_name_plural = 'Ticket linked Items'


    class Modules(models.IntegerChoices):
        CLUSTER          = 1, 'Cluster'
        CONFIG_GROUP     = 2, 'Config Group'
        DEVICE           = 3, 'Device'
        OPERATING_SYSTEM = 4, 'Operating System'
        SERVICE          = 5, 'Service'
        SOFTWARE         = 6, 'Software'

    is_global = None

    model_notes = None

    id = models.AutoField(
        blank=False,
        help_text = 'ID Number',
        primary_key=True,
        unique=True,
        verbose_name = 'Number',
    )

    ticket = models.ForeignKey(
        Ticket,
        blank= False,
        help_text = 'Ticket the item will be linked to',
        null = False,
        on_delete = models.CASCADE,
        verbose_name = 'Ticket',
    )

    item_type = models.IntegerField(
        blank= False,
        choices = Modules,
        help_text = 'Python Model location for linked item',
        null = False,
        verbose_name = 'Item Type',
    )

    item = models.IntegerField(
        blank = False,
        help_text = 'Item ID to link to ticket',
        null = False,
        verbose_name = 'Item ID',
    )

    table_fields: list = []

    def __str__(self) -> str:

        item_type: str = None

        if self.item_type == TicketLinkedItem.Modules.CLUSTER:

            item_type = 'cluster'

        elif self.item_type == TicketLinkedItem.Modules.CONFIG_GROUP:

            item_type = 'config_group'

        elif self.item_type == TicketLinkedItem.Modules.DEVICE:

            item_type = 'device'

        elif self.item_type == TicketLinkedItem.Modules.OPERATING_SYSTEM:

            item_type = 'operating_system'

        elif self.item_type == TicketLinkedItem.Modules.SERVICE:

            item_type = 'service'

        elif self.item_type == TicketLinkedItem.Modules.SOFTWARE:

            item_type = 'software'

        if item_type:

            return f'${item_type}-{int(self.item)}'

        return str(self.item)


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.ticket


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        request = get_request()

        if request:

            if request.user.pk:

                comment_user = request.user

            else:

                comment_user = None

        else:

            comment_user = None


        from core.models.ticket.ticket_comment import TicketComment

        comment = TicketComment.objects.create(
            ticket = self.ticket,
            comment_type = TicketComment.CommentType.ACTION,
            body = f'linked {self}',
            source = TicketComment.CommentSource.DIRECT,
            user = comment_user,
        )

        comment.save()
