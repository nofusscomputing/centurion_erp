from rest_framework import serializers
from rest_framework.reverse import reverse

from drf_spectacular.utils import extend_schema_serializer

from access.serializers.entity import BaseSerializer as EntityBaseSerializer
from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from centurion.serializers.user import UserBaseSerializer

from core import exceptions as centurion_exception
from core import fields as centurion_field
from core.fields.badge import BadgeField
from core.models.ticket_base import TicketBase
from core.serializers.ticket_category import TicketCategoryBaseSerializer

from project_management.serializers.project import ProjectBaseSerializer
from project_management.serializers.project_milestone import ProjectMilestoneBaseSerializer



@extend_schema_serializer(component_name = 'TicketBaseBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):
    """Base Ticket Model"""


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = TicketBase

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



@extend_schema_serializer(component_name = 'TicketBaseModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """Ticket Base Model"""


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        ticket_type = str(item.ticket_type)

        url_dict: dict = {
            '_self': item.get_url( request = self._context['view'].request ),
            'comments': reverse('v2:_api_ticket_comment_base-list', request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
            'linked_items': reverse("v2:_api_v2_ticket_linked_item-list", request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
        }

        if item.project:

            url_dict.update({
                'project': reverse("v2:_api_project-list", request=self._context['view'].request, kwargs={}),
            })

        if item.category:

            url_dict.update({
            'ticketcategory': reverse(
                'v2:_api_ticketcategory-list',
                request=self._context['view'].request,
                kwargs={},
            ) + '?' + ticket_type + '=true',
            })


        url_dict.update({
            'related_tickets': reverse("v2:_api_v2_ticket_related-list", request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
        })


        return url_dict

    description = centurion_field.MarkdownField( required = True, style_class = 'large' )

    impact_badge = BadgeField(label='Impact')

    organization = common.OrganizationField(
        required = True,
        write_only = True,
    )

    priority_badge = BadgeField(
        label = 'Priority',
        read_only = True,
    )

    status_badge = BadgeField(
        label = 'Status',
        read_only = True,
    )

    ticket_duration = serializers.IntegerField(
        help_text = 'Total time spent on ticket',
        label = 'Time Spent',
        read_only = True,
    )

    ticket_estimation = serializers.IntegerField(
        help_text = 'Time estimation to complete the ticket',
        label = 'Time estimation',
        read_only = True,
    )

    urgency_badge = BadgeField(
        label = 'Urgency',
        read_only = True,
    )


    class Meta:

        model = TicketBase

        fields = [
            'id',
            'display_name',
            'organization',
            'external_system',
            'external_ref',
            'parent_ticket',
            'ticket_type',
            'status',
            'status_badge',
            'category',
            'title',
            'description',
            'ticket_duration',
            'ticket_estimation',
            'project',
            'milestone',
            'urgency',
            'urgency_badge',
            'impact',
            'impact_badge',
            'priority',
            'priority_badge',
            'opened_by',
            'subscribed_to',
            'assigned_to',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'is_deleted',
            'is_solved',
            'date_solved',
            'is_closed',
            'date_closed',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if self.context.get('view', None) is not None:

            read_only_fields = [
                'id',
                'display_name',
                'created',
                'modified',
                '_urls',
            ]

            if not self.context['view']._has_import:

                read_only_fields += [
                    'external_system',
                    'external_ref',
                    'ticket_type',
                ]

            self.Meta.read_only_fields = read_only_fields


    def validate_field_milestone( self, attrs, raise_exception = False ) -> bool:

        milestone = attrs.get('milestone', None)

        project = attrs.get('project', None)

        if milestone is not None:

            if project is None:

                raise centurion_exception.ValidationError(
                    detail = {
                        'milestone': 'Milestones require a project'
                    },
                    code = 'milestone_requires_project',
                )


            elif project.id != milestone.project.id:

                del attrs['milestone']

                raise centurion_exception.ValidationError(
                    detail = {
                        'milestone': 'Milestone must be from the same project'
                    },
                    code = 'milestone_same_project',
                )

        return attrs


    def validate_field_external_system( self, attrs, raise_exception = False ) -> bool:

        external_system = attrs.get('external_system', None)

        external_ref = attrs.get('external_ref', None)

        if external_system is None and external_ref is not None:

            raise centurion_exception.ValidationError(
                detail = {
                    'external_system': 'External System is required when an External Ref is defined'
                },
                code = 'external_system_missing',
            )

        elif external_system is not None and external_ref is None:

            raise centurion_exception.ValidationError(
                detail = {
                    'external_ref': 'External Ref is required when an External System is defined'
                },
                code = 'external_ref_missing',
            )


        return attrs


    def validate(self, attrs):


        if getattr(self.context['view'], 'action', '') in [ 'create' ]:
            # Always set that the ticket was opened by user ho is making the request

            try:
                attrs['opened_by'] = self.context['request'].user
            except KeyError:
                pass


        attrs = self.validate_field_milestone( attrs )

        attrs = self.validate_field_external_system( attrs )

        attrs = super().validate( attrs )

        has_import_permission = self.context['view']._has_import

        has_triage_permission = self.context['view']._has_triage

        status = int(attrs.get('status', 0))

        opened_by_id = attrs.get('opened_by', 0)

        if opened_by_id != 0:

            opened_by_id = opened_by_id.id

        request_user_id = int(self.context['request'].user.id)

        if opened_by_id == 0:

            request_user_id = 0

        if not (
            has_triage_permission
            or has_import_permission
        ):

            if(
                status == TicketBase.TicketStatus.ASSIGNED
                or status == TicketBase.TicketStatus.ASSIGNED_PLANNING
            ):

                raise centurion_exception.ValidationError(
                    detail = {
                        'status': 'You cant assign a ticket if you dont have permission triage'
                    },
                    code = 'no_triage_status_assigned',
                )

            if status == TicketBase.TicketStatus.PENDING:

                raise centurion_exception.ValidationError(
                    detail = {
                        'status': 'You cant set a ticket to pending if you dont have permission triage'
                    },
                    code = 'no_triage_status_pending',
                )

            if(
                status == TicketBase.TicketStatus.SOLVED
                and opened_by_id != request_user_id
            ):

                raise centurion_exception.ValidationError(
                    detail = {
                        'status': 'You cant solve a ticket if you dont have permission triage'
                    },
                    code = 'no_triage_status_solve',
                )

            if(
                status == TicketBase.TicketStatus.INVALID
                and opened_by_id != request_user_id
            ):

                raise centurion_exception.ValidationError(
                    detail = {
                        'status': 'You cant mark a ticket as invalid if you did not raise the ticket or you dont have permission triage'
                    },
                    code = 'no_triage_status_invalid',
                )

            if status == TicketBase.TicketStatus.CLOSED:

                raise centurion_exception.ValidationError(
                    detail = {
                        'status': 'You cant close a ticket if you dont have permission triage'
                    },
                    code = 'no_triage_status_close',
                )


        elif (
            has_triage_permission
            or has_import_permission
        ):

            if(
                (
                    'status' not in attrs
                    or attrs.get('status', 0) == self.Meta.model.TicketStatus.NEW
                )
                and 'assigned_to' in attrs
            ):

                attrs['status'] = self.Meta.model.TicketStatus.ASSIGNED


        return attrs


    def is_valid(self, raise_exception = False):

        is_valid = super().is_valid( raise_exception = raise_exception )

        return is_valid



@extend_schema_serializer(component_name = 'TicketBaseViewSerializer')
class ViewSerializer(ModelSerializer):
    """Ticket Base View Model"""

    assigned_to = EntityBaseSerializer(many=True, label = 'assigned to')

    category = TicketCategoryBaseSerializer(label = 'category')

    milestone = ProjectMilestoneBaseSerializer(many=False, read_only=True)

    opened_by = UserBaseSerializer()

    organization = TenantBaseSerializer(many=False, read_only=True)

    parent_ticket = BaseSerializer()

    project = ProjectBaseSerializer(many=False, read_only=True)

    subscribed_to = EntityBaseSerializer(many=True, label = 'subscribved to')
