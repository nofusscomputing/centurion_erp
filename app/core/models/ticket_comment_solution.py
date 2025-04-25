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

        super().clean()


