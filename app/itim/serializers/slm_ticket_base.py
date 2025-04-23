from drf_spectacular.utils import extend_schema_serializer

from core.serializers.ticket import (
    BaseSerializer as TicketBaseSerializer,
    ModelSerializer as TicketModelSerializer,
    ViewSerializer as TicketViewSerializer
)

from itim.models.slm_ticket_base import SLMTicket



@extend_schema_serializer(component_name = 'SLMTicketBaseBaseSerializer')
class BaseSerializer(
    TicketBaseSerializer
):
    pass


@extend_schema_serializer(component_name = 'SLMTicketBaseModelSerializer')
class ModelSerializer(
    TicketModelSerializer,
    BaseSerializer
):
    """SLM Ticket Base Model"""

    class Meta:

        model = SLMTicket

        fields = [
            'id',
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
            'tto',
            'ttr',
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
            'external_system',
            'external_ref',
            'ticket_type',
            'tto',
            'ttr',
            'is_deleted',
            'created',
            'modified',
            '_urls',
        ]





@extend_schema_serializer(component_name = 'SLMTicketBaseViewSerializer')
class ViewSerializer(
    TicketViewSerializer,
    ModelSerializer,
    ):
    """SLM Ticket Base View Model"""

    pass
