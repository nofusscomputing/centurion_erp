from drf_spectacular.utils import extend_schema_serializer

from itim.serializers.ticketbase_slm import (
    BaseSerializer as SLMTicketBaseSerializer,
    ModelSerializer as SLMTicketModelSerializer,
    ViewSerializer as SLMTicketViewSerializer
)

from project_management.models.ticket_project_task import ProjectTaskTicket



@extend_schema_serializer(component_name = 'ProjectTaskTicketBaseSerializer')
class BaseSerializer(
    SLMTicketBaseSerializer
):
    pass


@extend_schema_serializer(component_name = 'ProjectTaskTicketModelSerializer')
class ModelSerializer(
    SLMTicketModelSerializer,
    BaseSerializer,
):
    """Service ProjectTask Ticket"""

    class Meta:

        model = ProjectTaskTicket

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
            'external_system',
            'external_ref',
            'ticket_type',
            'is_deleted',
            'created',
            'modified',
            '_urls',
        ]





@extend_schema_serializer(component_name = 'ProjectTaskTicketViewSerializer')
class ViewSerializer(
    SLMTicketViewSerializer,
    ModelSerializer,
    ):
    """Service ProjectTask Ticket View Model"""

    pass
