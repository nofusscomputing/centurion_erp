from django.core.exceptions import ValidationError
from django.db import models

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


    table_fields: list = [
        'id',
        'title',
        'status_badge',
        'opened_by',
        'organization',
        'created'
    ]



    def clean_fields(self, exclude=None):

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

        if obj.count() > 0:

            raise ValidationError(
                detail = {
                    'dependent_ticket': f"Ticket is already related to #{self.dependent_ticket.id}"
                },
                code = 'duplicate_entry'
            )

        if self.ticket == self.dependent_ticket:

            raise ValidationError(
                detail = {
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


    def __str__(self):

        return str( '#' + str(self.ticket.id) )
