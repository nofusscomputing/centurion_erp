from django.db import models

from core.models.ticket_comment_action import TicketCommentAction
from core.models.ticket_dependencies import TicketDependency


class TicketCommentActionTicketDependency(
    TicketCommentAction,
):


    @property
    def _base_model(self):

        return TicketCommentAction



    class Meta:

        ordering = [
            'id'
        ]

        permissions = [
            (
                'import_ticketcommentactionticketdependency',
                'Can import ticket dependency action comment.'
            ),
        ]

        verbose_name = "Ticket Dependency Action Comment"

        verbose_name_plural = "Ticket Dependency Action Comments"


    is_create = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'is this an add operation?',
        verbose_name = 'Adding link'
    )

    link_type = models.IntegerField(
        blank = False,
        choices = TicketDependency.Related,
        help_text = 'How is the ticket related',
        verbose_name = 'How Related',
    )

    dependent_ticket_id = models.IntegerField(
        blank = False,
        default = 0,
        help_text = 'ID of ticket',
        null = False,
        verbose_name = 'Ticket ID',
    )



    def __str__(self):

        comment = f"{self.user} added {self.dependent_ticket_id} as " \
            f"{self.get_link_type_display()}"

        if not self.is_create:

            comment = f"{self.user} removed {self.dependent_ticket_id} as " \
                f"{self.get_link_type_display()}"


        return comment
