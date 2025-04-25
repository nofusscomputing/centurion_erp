from django.apps import apps
from django.db import models

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.entity import Entity
from access.models.tenancy import TenancyObject

from core import exceptions as centurion_exception
from core.lib.feature_not_used import FeatureNotUsed
from core.lib.slash_commands import SlashCommands
from core.models.ticket_base import TicketBase
from core.models.ticket.ticket_comment_category import TicketCommentCategory



class TicketCommentBase(
    SlashCommands,
    TenancyObject
):


    save_model_history: bool = False


    class Meta:

        ordering = [
            'id'
        ]

        unique_together = ('external_system', 'external_ref',)

        sub_model_type = 'comment'

        verbose_name = "Ticket Comment"

        verbose_name_plural = "Ticket Comments"



    model_notes = None

    is_global = None


    id = models.AutoField(
        blank = False,
        help_text = 'Comment ID Number',
        primary_key = True,
        unique = True,
        verbose_name = 'Number',
    )

    parent = models.ForeignKey(
        'self',
        blank = True,
        default = None,
        help_text = 'Parent ID for creating discussion threads',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Parent Comment',
    )

    ticket = models.ForeignKey(
        TicketBase,
        blank = False,
        help_text = 'Ticket this comment belongs to',
        null = False,
        on_delete = models.PROTECT,
        verbose_name = 'Ticket',
    )

    external_ref = models.IntegerField(
        blank = True,
        default = None,
        help_text = 'External System reference',
        null = True,
        verbose_name = 'Reference Number',
    ) # external reference or null. i.e. github issue number

    external_system = models.IntegerField(
        blank = True,
        choices=TicketBase.Ticket_ExternalSystem,
        default=None,
        help_text = 'External system this item derives',
        null=True,
        verbose_name = 'External System',
    )

    @property
    def get_comment_type(self):

        comment_type = str(self.Meta.verbose_name).lower().replace(
            ' ', '_'
        )

        return comment_type

    def get_comment_type_choices():

        choices = []

        if apps.ready:

            all_models = apps.get_models()

            for model in all_models:

                if isinstance(model, TicketCommentBase) or issubclass(model, TicketCommentBase):

                    choices += [ (model._meta.sub_model_type, model._meta.verbose_name) ]


        return choices

    comment_type = models.CharField(
        blank = False,
        choices = get_comment_type_choices,
        # default = get_comment_type,
        help_text = 'Type this comment is. derived from Meta.verbose_name',
        max_length = 30,
        null = False,
        verbose_name = 'Type',
    ) 

    category = models.ForeignKey(
        TicketCommentCategory,
        blank = True,
        default = None,
        help_text = 'Category of the comment',
        null = True,
        on_delete = models.PROTECT,
        verbose_name = 'Category',
    )

    body = models.TextField(
        blank = True,
        help_text = 'Comment contents',
        null = True,
        verbose_name = 'Comment',
    )

    private = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this comment private',
        null = False,
        verbose_name = 'Private',
    )

    duration = models.IntegerField(
        blank = False,
        default = 0,
        help_text = 'Time spent in seconds',
        null = False,
        verbose_name = 'Duration',
    )

    estimation = models.IntegerField(
        blank = False,
        default = 0,
        help_text = 'Time estimation in seconds',
        null = False,
        verbose_name = 'Estimate',
    )

    template = models.ForeignKey(
        'self',
        blank= True,
        default = None,
        help_text = 'Comment Template to use',
        null = True,
        on_delete = models.SET_NULL,
        related_name = 'comment_template',
        verbose_name = 'Template',
    )

    is_template = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this comment a template',
        null = False,
        verbose_name = 'Template',
    )

    source = models.IntegerField(
        blank = False,
        choices = TicketBase.TicketSource,
        default = TicketBase.TicketSource.HELPDESK,
        help_text = 'Origin type for this comment',
        null = False,
        verbose_name = 'Source',
    ) 

    user = models.ForeignKey(
        Entity,
        blank= False,
        help_text = 'Who made the comment',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'comment_user',
        verbose_name = 'User',
    )

    is_closed = models.BooleanField(
        blank = False,
        default = False,
        help_text = 'Is this comment considered Closed?',
        null = False,
        verbose_name = 'Comment Closed',
    )

    date_closed = models.DateTimeField(
        blank = True,
        help_text = 'Date ticket closed',
        null = True,
        verbose_name = 'Closed Date',
    )

    created = AutoCreatedField(
        editable = True,
    )

    modified = AutoLastModifiedField()

    # this model is not intended to be viewable on its
    # own page due to being a sub model
    page_layout: list = []


    # this model is not intended to be viewable via
    # a table as it's a sub-model
    table_fields: list = []


    def clean(self):

        if not self.is_template:

            if self.is_closed and self.date_closed is None:

                raise centurion_exception.ValidationError(
                    detail = {
                        'date_closed': 'Ticket has been marked as closed and field date_closed is empty.'
                    },
                    code = 'ticket_closed_no_date'
                )

            
            try:
            
                self.ticket.get_can_resolve(raise_exceptions = True)

            except centurion_exception.ValidationError as err:

                raise centurion_exception.ValidationError(
                    detail = {
                        'body': err.detail['status']
                    },
                    code = err.code
                )


    def get_url_kwargs_notes(self):

        return FeatureNotUsed


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.ticket


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        self.organization = self.ticket.organization

        body = self.body

        self.body = self.slash_command(self.body)

        if(
           (
                (
                    body is not None
                    and body != ''
                )
                and (
                    self.body is not None
                    and self.body != ''
                )
            )
            or self.comment_type == self.CommentType.SOLUTION
        ):

            super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

            # if self.comment_type == self.CommentType.SOLUTION:

            #     update_ticket =  self.ticket.__class__.objects.get(pk=self.ticket.id)
            #     update_ticket.status = int(TicketBase.TicketStatus.All.SOLVED.value)

            #     update_ticket.save()