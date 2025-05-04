from rest_framework import serializers

from app.serializers.user import UserBaseSerializer

from core.models.ticket.ticket_category import TicketCategory
from core.serializers.ticket_depreciated import (
    Ticket,
    TicketBaseSerializer,
    TicketModelSerializer,
    TicketViewSerializer
)



class IncidentTicketBaseSerializer(
    TicketBaseSerializer
):

    class Meta( TicketBaseSerializer.Meta ):

        pass



class IncidentTicketModelSerializer(
    TicketModelSerializer,
    IncidentTicketBaseSerializer,
):

    category = serializers.PrimaryKeyRelatedField(
        allow_null = True,
        queryset = TicketCategory.objects.filter(
            incident = True
        ),
        required = False
    )

    status = serializers.ChoiceField(
        [(e.value, e.label) for e in Ticket.TicketStatus.Incident],
        default = Ticket.TicketStatus.All.NEW,
        required = False,
    )


    class Meta( TicketModelSerializer.Meta ):

        fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'parent_ticket',
            'created',
            'modified',
            'status',
            'status_badge',
            'title',
            'description',
            'estimate',
            'duration',
            'urgency',
            'urgency_badge',
            'impact',
            'impact_badge',
            'priority',
            'priority_badge',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'opened_by',
            'organization',
            'project',
            'milestone',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'parent_ticket',
            'external_ref',
            'external_system',
            'opened_by',
            'status_badge',
            'ticket_type',
            '_urls',
        ]



class IncidentAddTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Add` user

    Args:
        IncidentTicketModelSerializer (class): Model Serializer
    """


    category = serializers.PrimaryKeyRelatedField(
        read_only = True,
    )


    class Meta(IncidentTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'status_badge',
            'estimate',
            'duration',
            'impact',
            'priority',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'opened_by',
            'project',
            'milestone',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]



class IncidentChangeTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Incident` user

    Args:
        IncidentTicketModelSerializer (class): Incident Model Serializer
    """


    category = serializers.PrimaryKeyRelatedField(
        read_only = True,
    )

    status = serializers.ChoiceField(
        [(e.value, e.label) for e in Ticket.TicketStatus.Incident],
        read_only = True,
    )


    class Meta(IncidentTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'status_badge',
            'estimate',
            'duration',
            'impact',
            'priority',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'opened_by',
            'organization',
            'project',
            'milestone',
            'subscribed_teams',
            'subscribed_users',
            '_urls',
        ]



class IncidentTriageTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Triage` user

    Args:
        IncidentTicketModelSerializer (class): Incident Model Serializer
    """


    class Meta(IncidentTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'created',
            'modified',
            'status_badge',
            'estimate',
            'duration',
            'external_ref',
            'external_system',
            'ticket_type',
            'is_deleted',
            'date_closed',
            'opened_by',
            '_urls',
        ]



class IncidentImportTicketModelSerializer(
    IncidentTicketModelSerializer,
):
    """Serializer for `Import` user

    Args:
        IncidentTicketModelSerializer (class): Incident Model Serializer
    """

    class Meta(IncidentTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'display_name',
            'status_badge',
            'ticket_type',
            '_urls',
        ]


    is_import: bool = True



class IncidentTicketViewSerializer(
    TicketViewSerializer,
    IncidentTicketModelSerializer,
):

    pass
