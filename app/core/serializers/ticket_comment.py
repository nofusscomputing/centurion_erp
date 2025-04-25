import datetime

from rest_framework.reverse import reverse

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common
from api.exceptions import UnknownTicketType

from app.serializers.user import UserBaseSerializer

from core import exceptions as centurion_exceptions
from core import fields as centurion_field
from core.models.ticket_comment_base import TicketCommentBase
from core.serializers.ticket import BaseSerializer as TicketBaseBaseSerializer
from core.serializers.ticket_comment_category import TicketCommentCategoryBaseSerializer



@extend_schema_serializer(component_name = 'TicketCommentBaseBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = TicketCommentBase

        fields = [
            'id',
            'display_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url',
        ]



@extend_schema_serializer(component_name = 'TicketCommentBaseModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer,
):
    """Base class for Ticket Comment Model

    Args:
        TicketCommentBaseSerializer (class): Base class for ALL commment types.

    Raises:
        UnknownTicketType: Ticket type is undetermined.
    """

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        if item.ticket:

            ticket_id = item.ticket.id

        else:

            raise UnknownTicketType()


        urls: dict = {
            '_self': item.get_url( request = self._context['view'].request )
        }

        if item.id is not None:

            threads = TicketCommentBase.objects.filter(parent = item.id, ticket = ticket_id)

            if len(threads) > 0:

                urls.update({
                    'threads': reverse(
                        'API:_api_v2_ticket_comment_base_sub_thread-list',
                        request = self._context['view'].request,
                        kwargs={
                            'ticket_id': ticket_id,
                            'ticket_comment_model': 'comment',
                            'parent_id': item.id
                        }
                    )
                })

        return urls


    body = centurion_field.MarkdownField( required = True )


    class Meta:

        model = TicketCommentBase

        fields = '__all__'

        fields = [
            'id',
            'organization',
            'parent',
            'ticket',
            'external_ref',
            'external_system',
            'comment_type',
            'category',
            'body',
            'private',
            'duration',
            'estimation',
            'template',
            'is_template',
            'source',
            'user',
            'is_closed',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',

            #
            # Commented out as the metadata was not being populated.
            # ToDo: Unit test to confirm that this serializer is ONLY provided
            # to the metadata (HTTP/OPTIONS)
            #
            # 'parent',
            'external_ref',
            'external_system',
            # 'comment_type',
            # 'private',
            'duration',
            # # 'category',
            # 'template',
            # 'is_template',
            # 'source',
            # 'status',
            # 'responsible_user',
            # 'responsible_team',
            # 'user',
            # 'planned_start_date',
            # 'planned_finish_date',
            # 'real_start_date',
            # 'real_finish_date',
            'organization',
            # 'date_closed',
            'created',
            'modified',
            '_urls',
        ]


    is_triage: bool = False
    """ If the serializers is a Triage serializer"""

    def validate(self, attrs):

        attrs['comment_type'] = self.context['view'].model._meta.sub_model_type

        if attrs['comment_type'] == 'comment':

            attrs['is_closed'] = True
            attrs['date_closed'] = datetime.datetime.now(tz=datetime.timezone.utc).replace(microsecond=0).isoformat()

        if self.is_triage:

            attrs = self.validate_triage(attrs)


        return attrs




    def is_valid(self, *, raise_exception=False):

        is_valid: bool = False

        is_valid = super().is_valid(raise_exception=raise_exception)

        if self.context['view'].action == 'create':

            if 'ticket_id' in self._kwargs['context']['view'].kwargs:

                self.validated_data['ticket_id'] = int(self._kwargs['context']['view'].kwargs['ticket_id'])

                if 'parent_id' in self._kwargs['context']['view'].kwargs:

                    self.validated_data['parent_id'] = int(self._kwargs['context']['view'].kwargs['parent_id'])

                    comment = self.Meta.model.objects.filter( id = self.validated_data['parent_id'] )

                    if list(comment)[0].parent_id:

                        raise centurion_exceptions.ValidationError(
                            detail = {
                                'parent': 'Replying to a discussion reply is not possible'
                            },
                            code = 'single_discussion_replies_only'
                        )

            else:

                raise centurion_exceptions.ValidationError(
                    detail = {
                        'ticket': 'Ticket is a required field'
                    },
                    code = 'required'
                )

        return is_valid



@extend_schema_serializer(component_name = 'TicketCommentBaseViewSerializer')
class ViewSerializer(ModelSerializer):

    category = TicketCommentCategoryBaseSerializer( many = False, read_only = True )

    organization = OrganizationBaseSerializer( many = False )

    parent = BaseSerializer()

    template = BaseSerializer()

    ticket = TicketBaseBaseSerializer()

    user = UserBaseSerializer()
