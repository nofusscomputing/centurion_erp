from django.db import models
from django.conf import settings

from core.models.ticket_comment_base import TicketCommentBase



class TicketCommentTask(
    TicketCommentBase,
):

    _is_submodel = True

    class Meta:

        ordering = [
            'id'
        ]

        permissions = [
            ('import_ticketcommenttask', 'Can import ticket task comment.'),
            ('purge_ticketcommenttask', 'Can purge ticket task comment.'),
            ('triage_ticketcommenttask', 'Can triage ticket task comment.'),
        ]

        sub_model_type = 'task'

        verbose_name = "Ticket Comment Task"

        verbose_name_plural = "Ticket Comment Task"



    class CommentStatus(models.IntegerChoices):
        """Comment Completion Status"""

        TODO = '1', 'To Do'
        DONE = '2', 'Done'



    status = models.IntegerField(
        blank = False,
        choices=CommentStatus,
        default = CommentStatus.TODO,
        help_text = 'Status of task',
        verbose_name = 'Status',
    ) 

    assignee = models.ForeignKey(
        'access.Entity',
        blank = True,
        default = None,
        help_text = 'whom is responsible for the completion of comment',
        on_delete = models.PROTECT,
        related_name = '+',
        null = True,
        verbose_name = 'Assignee',
    )

    planned_start_date = models.DateTimeField(
        blank = True,
        help_text = 'Planned start date.',
        null = True,
        verbose_name = 'Planned Start Date',
    )

    planned_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'Planned finish date',
        null = True,
        verbose_name = 'Planned Finish Date',
    )

    real_start_date = models.DateTimeField(
        blank = True,
        help_text = 'Real start date',
        null = True,
        verbose_name = 'Real Start Date',
    )

    real_finish_date = models.DateTimeField(
        blank = True,
        help_text = 'Real finish date',
        null = True,
        verbose_name = 'Real Finish Date',
    )

    is_deleted = models.BooleanField(
        blank = True,
        default = False,
        help_text = 'Is the comment deleted? And ready to be purged',
        null = False,
        verbose_name = 'Deleted',
    )
