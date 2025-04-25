import datetime


from core import exceptions as centurion_exception
from core.models.ticket_comment_base import TicketCommentBase



class TicketCommentSolution(
    TicketCommentBase,
):

    class Meta:

        ordering = [
            'id'
        ]

        sub_model_type = 'solution'

        verbose_name = "Ticket Comment Solution"

        verbose_name_plural = "Ticket Comment Solutions"


    def clean(self):

        if self.ticket.is_solved:

            raise centurion_exception.ValidationError(
                detail = 'Ticket is already solved',
                code = 'ticket_already_solved'
            )


        super().clean()


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.is_closed = True

        self.date_closed = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

        self.ticket.is_solved = self.is_closed

        self.ticket.date_solved = self.date_closed

        self.ticket.status = self.ticket.TicketStatus.SOLVED

        self.ticket.save()

        super().save(force_insert = force_insert, force_update = force_update, using = using, update_fields = update_fields)


