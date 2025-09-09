from rest_framework.reverse import reverse

from rest_framework import serializers

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.entity import BaseSerializer as EntityBaseSerializer
from access.serializers.organization import TenantBaseSerializer

from api.serializers import common
from api.exceptions import UnknownTicketType


from core import exceptions as centurion_exceptions
from core import fields as centurion_field
from core.models.ticket_comment_base import TicketCommentBase
from core.serializers.ticketbase import BaseSerializer as TicketBaseBaseSerializer
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
                        'API:_api_ticket_comment_base_sub_thread-list',
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



    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if 'context' not in kwargs:
            return

        if getattr(kwargs['context'].get('view'), 'action', '') in ['create', 'partial_update', 'update']:

            self.fields.fields['parent'].write_only = True
            self.fields.fields['ticket'].write_only = True
            self.fields.fields['user'].write_only = True

        if self.context.get('view', None) is not None:

            read_only_fields = [
                'id',
                'display_name',
                '_urls',
            ]

            if not self.context['view']._has_import:

                read_only_fields += [
                    'created',
                    'modified',
                    'organization'
                    'external_system',
                    'external_ref',
                    'duration',
                ]

            if(
                not self.context['view']._has_import
                and not self.context['view']._has_triage
            ):

                read_only_fields += [
                    'category',
                    'source',
                ]

            self.Meta.read_only_fields = read_only_fields



    def validate_triage(self, attrs):

        return attrs


    def validate_new_comment(self, attrs):

        # attrs['user'] = self.context['request'].user


        if 'ticket_id' in self.context['view'].kwargs:

            attrs['ticket_id'] = int(self.context['view'].kwargs['ticket_id'])


            if 'parent_id' in self.context['view'].kwargs:

                attrs['parent_id'] = int(self.context['view'].kwargs['parent_id'])

                comment = self.Meta.model.objects.filter( id = attrs['parent_id'] )


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
                            'parent': 'Replying to a discussion reply is not possible'
                        },
                        code = 'single_discussion_replies_only'
                    )

        return attrs



    def validate_update_comment(self, attrs):

        if self.instance.user != self.context['request'].user:    # Owner Edit

            if 'private' in attrs:

                if self.instance.private:

                    raise centurion_exceptions.ValidationError(
                        detail = {
                            'private': 'Once a comment is made private it can\'t be undone.'
                        },
                        code = 'owner_cant_remove_private'
                    )


        return attrs




    def validate(self, attrs):

        attrs['comment_type'] = self.context['view'].model._meta.sub_model_type

        if self.context['view']._has_triage:

            attrs = self.validate_triage( attrs )


        if self.context['view'].action == 'create':

            attrs = self.validate_new_comment( attrs )

        elif self.context['view'].action in [ 'partial_update', 'update' ]:

            attrs = self.validate_update_comment( attrs )


        return attrs




    def is_valid(self, *, raise_exception=False):

        is_valid: bool = False

        is_valid = super().is_valid(raise_exception=raise_exception)

        return is_valid



@extend_schema_serializer(component_name = 'TicketCommentBaseViewSerializer')
class ViewSerializer(ModelSerializer):

    category = TicketCommentCategoryBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False )

    parent = BaseSerializer()

    template = BaseSerializer()

    ticket = TicketBaseBaseSerializer()

    user = EntityBaseSerializer()
