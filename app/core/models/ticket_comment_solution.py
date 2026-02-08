import datetime

from django.core.exceptions import (
    ValidationError
)
from core import exceptions as centurion_exception
from core.models.ticket_comment_base import TicketCommentBase



class TicketCommentSolution(
    TicketCommentBase,
):

    _is_submodel = True

    class Meta:

        ordering = [
            'id'
        ]

        permissions = [
            ('import_ticketcommentsolution', 'Can import ticket solution comment.'),
            ('purge_ticketcommentsolution', 'Can purge ticket solution comment.'),
        ]

        sub_model_type = 'solution'

        verbose_name = "Ticket Comment Solution"

        verbose_name_plural = "Ticket Comment Solutions"


    def clean(self):

        super().clean()

        if self.ticket.is_solved:

            raise ValidationError(
                message = 'Ticket is already solved',
                code = 'ticket_already_solved'
            )

        self.ticket.get_can_resolve(raise_exceptions = True)

        if self.parent:

            raise ValidationError(
                message = {
                    'parent': 'solution comment cant be added as a threaded comment'
                },
                code = 'solution_comment_not_threadable'
            )


    def clean_fields(self, exclude=None):

        self.is_closed = True

        self.date_closed = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

        super().clean_fields(exclude = exclude)



    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        super().save(force_insert = force_insert, force_update = force_update, using = using, update_fields = update_fields)

        self.ticket.status = self.ticket.TicketStatus.SOLVED

        self.ticket.save()

        # clear comment cache
        if hasattr(self.ticket, '_ticket_comments'):

            del self.ticket._ticket_comments
