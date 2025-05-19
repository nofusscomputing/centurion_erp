from core.models.ticket_comment_base import TicketCommentBase



class TicketCommentAction(
    TicketCommentBase,
):

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



    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

    #     super().save(force_insert = force_insert, force_update = force_update, using = using, update_fields = update_fields)

    #     self.ticket.is_solved = 

    #     self.ticket.date_solved = self.date_closed

    #     self.ticket.status = self.ticket.TicketStatus.SOLVED

    #     self.ticket.save()

    #     # clear comment cache
    #     if hasattr(self.ticket, '_ticket_comments'):

    #         del self.ticket._ticket_comments


