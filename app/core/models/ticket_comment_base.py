import datetime

from django.apps import apps
from django.db import models

from rest_framework.reverse import reverse

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

        permissions = [
            ('import_ticketcommentbase', 'Can import ticket comment.'),
            ('purge_ticketcommentbase', 'Can purge ticket comment.'),
            ('triage_ticketcommentbase', 'Can triage ticket comment.'),
        ]

        sub_model_type = 'comment'

        unique_together = ('external_system', 'external_ref',)

        verbose_name = "Ticket Comment"

        verbose_name_plural = "Ticket Comments"


    def field_validation_not_empty(value):

        if value == '' or value is None:

            raise centurion_exception.ValidationError(
                    detail = {
                        'comment_type': 'Comment Type requires a value.'
                    },
                    code = 'comment_type_empty_or_null'
                )

        return True


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
        help_text = 'External System reference',
        null = True,
        verbose_name = 'Reference Number',
    ) # external reference or null. i.e. github issue number

    external_system = models.IntegerField(
        blank = True,
        choices=TicketBase.Ticket_ExternalSystem,
        help_text = 'External system this item derives',
        null=True,
        verbose_name = 'External System',
    )

    @property
    def get_comment_type(self):

        comment_type = str(self._meta.sub_model_type).lower().replace(
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
        validators = [
            field_validation_not_empty
        ],
        verbose_name = 'Type',
    ) 

    category = models.ForeignKey(
        TicketCommentCategory,
        blank = True,
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

        try:
            self.organization

        except:
            self.organization = self.ticket.organization


        if not self.is_template:

            if self.is_closed and self.date_closed is None:

                self.date_closed = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()


            if self.comment_type != self._meta.sub_model_type:

                raise centurion_exception.ValidationError(
                    detail = {
                        'comment_type': 'Comment Type does not match. Check the http endpoint you are using.'
                    },
                    code = 'comment_type_wrong_endpoint'
                )



    def get_related_model(self):
        """Recursive model Fetch

        Returns the lowest model found in a chain of inherited models.

        Args:
            model (models.Model, optional): Model to fetch the child model from. Defaults to None.

        Returns:
            models.Model: Lowset model found in inherited model chain
        """

        related_model_name = self.get_related_field_name()

        related_model = getattr(self, related_model_name, None)

        if related_model_name == '':

            related_model = None

        elif related_model is None:

            related_model = self

        elif hasattr(related_model, 'get_related_field_name'):

            if related_model.get_related_field_name() != '':

                related_model = related_model.get_related_model()


        return related_model



    def get_related_field_name(self) -> str:

        meta = getattr(self, '_meta')

        for related_object in getattr(meta, 'related_objects', []):

            if not issubclass(related_object.related_model, TicketBase):

                continue

            if getattr(self, related_object.name, None):

                if( 
                    not str(related_object.name).endswith('history')
                    and not str(related_object.name).endswith('notes')
                ):

                    return related_object.name
                    break


        return ''



    def get_url( self, request = None ) -> str:

        kwargs = self.get_url_kwargs()

        if self.parent:

            url_name = '_api_v2_ticket_comment_base_sub_thread'

        else:

            url_name = '_api_v2_ticket_comment_base_sub'


        if request:

            return reverse('v2:' + url_name + '-detail', request=request, kwargs = kwargs )


        return reverse('v2:' + url_name + '-detail', kwargs = kwargs )



    def get_url_kwargs(self) -> dict:

        kwargs = {
            'ticket_comment_model': self.comment_type,
            'ticket_id': self.ticket.id,
        }

        if self.pk:

            kwargs.update({
                'pk': self.id
            })

        if self.parent:

            kwargs.update({
                'parent_id': self.parent.id
            })


        return kwargs


    def get_url_kwargs_notes(self):

        return FeatureNotUsed


    @property
    def parent_object(self):
        """ Fetch the parent object """
        
        return self.ticket


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

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

            # clear ticket comment cache
            if hasattr(self.ticket, '_ticket_comments'):

                del self.ticket._ticket_comments
