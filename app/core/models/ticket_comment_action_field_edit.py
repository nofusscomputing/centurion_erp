from django.db import models

from core.models.ticket_comment_action import TicketCommentAction



class TicketCommentActionFieldEdit(
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
                'import_ticketcommentactionfieldedit',
                'Can import ticket field change action comment.'
            ),
        ]

        verbose_name = "Ticket Field Change Action Comment"

        verbose_name_plural = "Ticket Field Change Action Comments"


    field_name = models.CharField(
        blank = False,
        help_text = 'Name of the field that was changed',
        max_length = 50,
        unique = False,
        verbose_name = 'Field Name'
    )

    previous_value = models.CharField(
        blank = True,
        help_text = 'Value changed from',
        max_length = 50,
        null = True,
        unique = False,
        verbose_name = 'Previous Value'
    )

    new_value = models.CharField(
        blank = True,
        help_text = 'Value changed to',
        max_length = 50,
        null = True,
        unique = False,
        verbose_name = 'New Value'
    )



    def __str__(self):

        comment = (
            f"Changed {self.field_name} changed from _{self.previous_value}_"
            f" to **{self.new_value}**"
        )

        if not self.previous_value:

            comment = (
                f"Set {self.field_name} to **{self.new_value}**"
            )

        elif not self.new_value:

            comment = (
                f"{self.user} removed ~~{self.previous_value}~~ "
                f"from {self.field_name}"
            )


        return comment
