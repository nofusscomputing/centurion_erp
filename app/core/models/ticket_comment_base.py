import datetime
import re

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from rest_framework.reverse import reverse

from access.fields import AutoCreatedField, AutoLastModifiedField
from access.models.entity import Entity

from core import exceptions as centurion_exception
from core.lib.slash_commands import SlashCommands
from core.models.centurion import CenturionModel
from core.models.ticket_base import TicketBase
from core.models.ticket.ticket_comment_category import TicketCommentCategory



class TicketCommentBase(
    SlashCommands,
    CenturionModel,
):


    _linked_model_kwargs: tuple[ tuple[ str ] ]  = (
        ( 'pk', ),
    )

    _audit_enabled = False

    @property
    def _base_model(self):

        return TicketCommentBase

    _notes_enabled = False

    _ticket_linkable = False

    model_notes = None

    model_tag = None

    save_model_history: bool = False

    url_model_name = 'ticket_comment_base'


    class Meta:

        ordering = [
            'id'
        ]

        permissions = [
            ('import_ticketcommentbase', 'Can import ticket comment.'),
            ('purge_ticketcommentbase', 'Can purge ticket comment.'),
        ]

        unique_together = ('external_system', 'external_ref',)

        verbose_name = "Ticket Comment"

        verbose_name_plural = "Ticket Comments"


    model_notes = None


    parent = models.ForeignKey(
        'self',
        blank = True,
        help_text = 'Parent ID for creating discussion threads',
        null = True,
        on_delete = models.PROTECT,
        related_name = 'threads',
        verbose_name = 'Parent Comment',
    )

    ticket = models.ForeignKey(
        TicketBase,
        blank = False,
        help_text = 'Ticket this comment belongs to',
        null = True,
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
    page_layout: dict = {}


    def clean(self):

        if not self.is_template:

            if(
                self.pk is None
                and self._meta.model_name == 'ticketcommentbase'
            ):
                self.is_closed = True

            if self.is_closed and self.date_closed is None:

                self.date_closed = datetime.datetime.now(tz=datetime.timezone.utc).replace(
                    microsecond=0).isoformat()

            elif not self.is_closed and self.date_closed is not None:
                self.date_closed = None


            if self.parent:

                if self.parent.parent:

                    raise ValidationError(
                        message = {
                            'parent': 'Replying to a discussion reply is not possible'
                        },
                        code = 'single_level_discussion_replies_only'
                    )

        super().clean()



    def clean_fields(self, exclude=None):

        self.organization = self.ticket.organization


        super().clean_fields(exclude = exclude)



    def delete(self, using = None, keep_parents = False):

        if len(self.threads.all()):
            raise models.ProtectedError(
                msg = 'Can not delete a comment that has threads',
                protected_objects = self
            )


        return super().delete(using = using, keep_parents = False)



    def get_url(
        self, relative: bool = True, api_version: int = 2, many = False
    ) -> str:

        namespace = f'v{api_version}'

        if self.get_app_namespace():
            namespace = namespace + ':' + self.get_app_namespace()


        url_basename = f'{namespace}:_api_{self._meta.model_name}'

        if self.url_model_name:

            url_basename = f'{namespace}:_api_{self.url_model_name}'

        if self._is_submodel:

            url_basename += '_sub'

        if self.parent:

            url_basename += '_thread'


        if many:

            url_basename += '-list'

        else:

            url_basename += '-detail'


        url = reverse( viewname = url_basename, request = None, kwargs = self.get_url_kwargs( many = many ) )

        if not relative:

            url = settings.SITE_URL + url


        return url



    def get_url_kwargs(self, many = False) -> dict:
        kwargs = {}

        if self._is_submodel:
            kwargs = {
                'model_name': self._meta.model_name
            }

        kwargs.update({
            'ticket_id': self.ticket.id,
        })

        if self.parent:

            kwargs.update({
                'parent_id': self.parent.id
            })


        if not many:

            kwargs.update({
                'pk': self.id
            })


        return kwargs



    @property
    def parent_object(self):
        """ Fetch the parent object """

        return self.ticket


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        body = self.body

        if self._meta.model_name != 'ticketcommentaction':
            self.body = self.slash_command(self.body)

        is_converted_action_comment = False
        action_comment_time_track = re.match(self.time_track, body)
        if(
            self.body != body
            and action_comment_time_track
            and self._meta.model_name == 'ticketcommentbase'
        ):

            is_converted_action_comment = True
           

            if action_comment_time_track:    # Time Tracking comment
                self.body = f"added {time_track.group('time')} of time spent"


        if(
           (
                body is not None
                and (
                    self.body is not None
                )
            )
            or self._meta.model_name == 'ticketcommentsolution'
        ):

            super().save(force_insert=force_insert, force_update=force_update,
                using=using, update_fields=update_fields)


            if is_converted_action_comment:

                action_comment = apps.get_model(
                    app_label = 'core',
                    model_name = 'ticketcommentaction'
                )(
                    id = self.id,
                    pk = self.id,
                    ticket = self.ticket
                )

                action_comment.full_clean()
                action_comment.save()


            # clear ticket comment cache
            if hasattr(self.ticket, '_ticket_comments'):

                del self.ticket._ticket_comments

            if self.parent:

                if(
                    self.parent.is_closed
                    and self._meta.model_name not in [ 'ticketcommentaction', 'ticketcommentsolution' ]
                ):

                    self.parent.is_closed = False
                    self.parent.save()