from drf_spectacular.utils import extend_schema_serializer

from itim.serializers.ticketbase_slm import (
    BaseSerializer as SLMTicketBaseSerializer,
    ModelSerializer as SLMTicketModelSerializer,
    ViewSerializer as SLMTicketViewSerializer
)

from itim.models.ticket_problem import ProblemTicket



@extend_schema_serializer(component_name = 'ProblemTicketBaseSerializer')
class BaseSerializer(
    SLMTicketBaseSerializer
):
    pass


@extend_schema_serializer(component_name = 'ProblemTicketModelSerializer')
class ModelSerializer(
    SLMTicketModelSerializer,
    BaseSerializer,
):
    """Service Problem Ticket"""

    class Meta:

        model = ProblemTicket

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
            'business_impact',
            'cause_analysis',
            'observations',
            'workaround',
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
            # 'tto',
            # 'ttr',
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
            # 'tto',
            # 'ttr',
            'is_deleted',
            'created',
            'modified',
            '_urls',
        ]





@extend_schema_serializer(component_name = 'ProblemTicketViewSerializer')
class ViewSerializer(
    SLMTicketViewSerializer,
    ModelSerializer,
    ):
    """Service Problem Ticket View Model"""

    pass
