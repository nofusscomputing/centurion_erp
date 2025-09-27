from django.contrib.auth.models import ContentType
from django.db import models
from django.utils.ipv6 import ValidationError

from access.fields import AutoLastModifiedField

from core.models.centurion import CenturionModel
from core.models.ticket_base import TicketBase



class ModelTicket(
    CenturionModel
):

    _audit_enabled = False

    _notes_enabled = False

    _ticket_linkable = False

    documentation = ''

    model_notes = None

    model_tag = None

    @property
    def url_model_name(self):
        return ModelTicket._meta.model_name


    class Meta:

        ordering = [
            'created'
        ]

        verbose_name = 'Ticket Linked Model'

        verbose_name_plural = 'Ticket Linked Models'


    content_type = models.ForeignKey(
        ContentType,
        blank= True,
        help_text = 'Model this history is for',
        null = False,
        on_delete = models.CASCADE,
        validators = [
            CenturionModel.validate_field_not_none,
        ],
        verbose_name = 'Content Model'
    )

    model = None    # is overridden with the model field in child-model

    ticket = models.ForeignKey(
        TicketBase,
        blank = False,
        help_text = 'Ticket object is linked to',
        null = False,
        on_delete = models.PROTECT,
        related_name = 'linked_models',
        verbose_name = 'Ticket',
    )

    modified = AutoLastModifiedField()


    page_layout: dict = []


    table_fields: list = [
        'organization',
        'ticket',
        'created',
    ]



    def __str__(self) -> str:

        return ''



    def get_url_kwargs(self, many = False):

        kwargs = super().get_url_kwargs( many = many )

        if not self._is_submodel:

            if kwargs.get('model_name', None):
                del kwargs['model_name']

            kwargs.update({
                'ticket_type': self.ticket._meta.sub_model_type,
                'model_id': self.ticket.id,
            })

        return kwargs


class ModelTicketMetaModel(
    ModelTicket,
):

    _is_submodel = True

    class Meta:

        abstract = True

        ordering = [
            'created'
        ]

        proxy = False

        unique_together = (
            'ticket',
            'model'
        )


    def clean_fields(self, exclude = None):

        if self.__class__.objects.filter(
            model_id = self.model.id, ticket_id = self.ticket.id
        ).exclude( id = getattr(self, 'id', 0)).exists():

            raise ValidationError(
                message = 'This object and ticket assignment already exists',
                code = 'no_duplicate_ticket_model'
            )

        self.organization = self.model.get_tenant()

        self.content_type = ContentType.objects.get(
            app_label = self.model._meta.app_label,
            model = self.model._meta.model_name
        )

        super().clean_fields(exclude = exclude)



    def get_url_kwargs(self, many = False):

        kwargs = super().get_url_kwargs( many = many )

        model_name = str(self._meta.model_name)
        if model_name.endswith('ticket') and len(model_name) > 6:
            model_name = str(model_name)[0:len(model_name)-len(str('ticket'))]

        kwargs.update({
            'app_label': self.model._meta.app_label,
            'model_name': str( model_name ),
            'model_id': self.model.id,
        })

        return kwargs
