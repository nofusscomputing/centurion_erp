from core.models.ticket_comment_base import TicketCommentBase



class TicketCommentAction(
    TicketCommentBase,
):

    _is_submodel = True

    class Meta:

        ordering = [
            'id'
        ]

        permissions = [
            ('import_ticketcommentaction', 'Can import ticket action comment.'),
        ]

        sub_model_type = 'action'

        verbose_name = "Ticket Comment Action"

        verbose_name_plural = "Ticket Comment Actions"


    def clean(self):

        self.is_closed = True

        super().clean()
