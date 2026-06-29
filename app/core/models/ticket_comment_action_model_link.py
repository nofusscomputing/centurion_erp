from django.contrib.auth.models import (
    ContentType,
)
from django.db import models

from core.models.ticket_comment_action import TicketCommentAction



class TicketCommentActionModelLink(
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
                'import_ticketcommentactionmodellink',
                'Can import ticket model link action comment.'
            ),
        ]

        verbose_name = "Ticket Linked Model Action Comment"

        verbose_name_plural = "Ticket Linked Model Action Comments"


    is_create = models.BooleanField(
        blank = False,
        default = True,
        help_text = 'is this an add operation?',
        verbose_name = 'Adding link'
    )

    model_id = models.IntegerField(
        blank = False,
        default = 0,
        help_text = 'ID of model',
        null = False,
        verbose_name = 'Model ID',
    )

    content_type = models.ForeignKey(
        to = ContentType,
        blank = False,
        help_text = 'Content ID of the model',
        null = False,
        on_delete = models.PROTECT,
        related_name = '+',
        verbose_name = 'Content ID for model',
    )



    def __str__(self):

        comment = f"Linked model ${self.content_type.model_class().model_tag}-{self.model_id}"

        if not self.is_create:

            comment = f"Unlinked model ${self.content_type.model_class().model_tag}-{self.model_id}"


        return comment
