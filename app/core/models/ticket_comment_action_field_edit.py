import difflib

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

    edit_type = models.IntegerField(
        blank = False,
        choices = [
            (0, 'Add'),
            (1, 'Edit'),
            (2, 'Remove'),
        ],
        default = 1,
        help_text = 'Enables distinguishing between m2m (Add, Remove) and other fields (Edit)',
        verbose_name = 'Edit Type'
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
            f"changed {self.ticket.get_related_model()._meta.get_field(self.field_name).verbose_name} from _{self.previous_value}_"
            f" to **{self.new_value}**"
        )

        if self.edit_type != 1:

            type_label = 'added'
            modifier = 'to'

            if self.edit_type == 2:

                type_label = 'removed'
                modifier = 'from'

            comment = (
                f"{type_label} {self.previous_value} {modifier} {self.new_value}"
            )

        if(
            not self.previous_value
            and isinstance(
                self.ticket.get_related_model()._meta.get_field(self.field_name),
                models.ForeignKey
            )
        ):

            comment = (
                f"set {self.ticket.get_related_model()._meta.get_field(self.field_name).verbose_name} to **{self.new_value}**"
            )

        elif not self.new_value:

            comment = (
                f"removed ~~{self.previous_value}~~ "
                f"from {self.ticket.get_related_model()._meta.get_field(self.field_name).verbose_name}"
            )


        if self.field_name == 'description':

            comment_field_value = ''.join(
                str(x) for x in list(
                    difflib.unified_diff(
                        str(self.previous_value + '\n').splitlines(keepends=True),
                        str(self.new_value + '\n').splitlines(keepends=True),
                        fromfile = 'before',
                        tofile = 'after',
                        n = 10000,
                        lineterm = '\n'
                    )
                )
            ) + ''

            comment = (
                '<details><summary>Changed the Description</summary>'
                    f'\n\n``` diff \n\n{comment_field_value}\n\n```\n\n'
                '</details>'
                )


        return comment
