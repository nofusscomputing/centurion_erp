from django.core.exceptions import ValidationError
from django.db import models

from access.models.entity import Entity

from core.models.centurion import CenturionModel
from core.models.ticket_base import TicketBase



class TicketDependency(
    CenturionModel
):

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False

    save_model_history: bool = False

    class Meta:

        ordering = [
            'id'
        ]

        verbose_name = 'Ticket Dependency'

        verbose_name_plural = 'Ticket Dependencies'


    class Related(models.IntegerChoices):

        RELATED    = '1', 'Related'
        BLOCKS     = '2', 'Blocks'
        BLOCKED_BY = '3', 'Blocked By'


    model_notes = None


    ticket = models.ForeignKey(
        TicketBase,
        blank = False,
        help_text = 'This Ticket',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'ticket',
        verbose_name = 'Ticket',
    )


    how_related = models.IntegerField(
        blank = False,
        choices = Related,
        help_text = 'How is the ticket related',
        verbose_name = 'How Related',
    )


    dependent_ticket = models.ForeignKey(
        TicketBase,
        blank = False,
        help_text = 'The Related Ticket',
        null = False,
        on_delete = models.CASCADE,
        related_name = 'dependent_ticket',
        verbose_name = 'Related Ticket',
    )

    user = models.ForeignKey(
        Entity,
        blank= False,
        help_text = 'Who added the dependency',
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'User',
    )


    table_fields: list = [
        'id',
        'title',
        'status_badge',
        'opened_by',
        'organization',
        'created'
    ]

    page_layout = None



    def __str__(self):

        return str( '#' + str(self.ticket.id) )



    def clean_fields(self, exclude=None):

        self.organization = self.ticket.organization

        model = type(self)


        obj = model.objects.filter(
            models.Q(
                ticket = self.ticket,
                dependent_ticket = self.dependent_ticket
            )
                |
            models.Q(
                ticket = self.dependent_ticket,
                dependent_ticket = self.ticket
            )
        )


        exclude = {}
        if self.pk:

            obj = obj.exclude(
                pk = self.pk
            )



        if obj.count() > 0:

            raise ValidationError(
                message = {
                    'dependent_ticket': f"Ticket is already related to #{self.dependent_ticket.id}"
                },
                code = 'duplicate_entry'
            )

        if self.ticket == self.dependent_ticket:

            raise ValidationError(
                message = {
                    'dependent_ticket': "Ticket can not be assigned to itself as related"
                },
                code = 'self_not_related'
            )


        return super().clean_fields(exclude)



    def get_url_kwargs(self, many = False) -> dict:

        kwargs = super().get_url_kwargs( many = many )

        kwargs['ticket_id'] = self.ticket.id

        return kwargs


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.ticket



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

        if self.how_related == self.Related.BLOCKED_BY:

            comment_field_value_from = f"added #{self.ticket.id} as blocked by #{self.dependent_ticket.id}"
            comment_field_value_to = f"added #{self.dependent_ticket.id} as blocking #{self.ticket.id}"

        elif self.how_related == self.Related.BLOCKS:

            comment_field_value_from = f"added #{self.ticket.id} as blocking #{self.dependent_ticket.id}"
            comment_field_value_to = f"added #{self.dependent_ticket.id} as blocked by #{self.ticket.id}"

        elif self.how_related == self.Related.RELATED:

            comment_field_value_from = f"added #{self.ticket.id} as related to #{self.dependent_ticket.id}"
            comment_field_value_to = f"added #{self.dependent_ticket.id} as related to #{self.ticket.id}"


        from core.models.ticket_comment_action import TicketCommentAction

        if comment_field_value_from:

            TicketCommentAction.objects.create(
                ticket = self.ticket,
                comment_type = TicketCommentAction._meta.sub_model_type,
                body = comment_field_value_from,
                source = TicketBase.TicketSource.DIRECT,
                user = self.user,
                is_closed = True,
            )


        if comment_field_value_to:

            TicketCommentAction.objects.create(
                ticket = self.dependent_ticket,
                comment_type = TicketCommentAction._meta.sub_model_type,
                body = comment_field_value_to,
                source = TicketBase.TicketSource.DIRECT,
                user = self.user,
                is_closed = True,
            )
