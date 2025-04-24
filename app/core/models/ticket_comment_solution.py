from core import exceptions as centurion_exception
from core.models.ticket_comment_base import TicketCommentBase



class TicketCommentSolution(
    TicketCommentBase,
):

    class Meta:

        ordering = [
            'id'
        ]

        verbose_name = "Solution"

        verbose_name_plural = "Solutions"


    def clean(self):

        super().clean()


