from rest_framework import serializers

from core.models.ticket.ticket_category import TicketCategory
from core.serializers.ticket_depreciated import (
    Ticket,
    TicketBaseSerializer,
    TicketModelSerializer,
    TicketViewSerializer
)



class ProblemTicketBaseSerializer(
    TicketBaseSerializer
):

    class Meta( TicketBaseSerializer.Meta ):

        pass



class ProblemTicketModelSerializer(
    TicketModelSerializer,
    ProblemTicketBaseSerializer,
):


    category = serializers.PrimaryKeyRelatedField(
        allow_null = True,
        queryset = TicketCategory.objects.filter(
            problem = True
        ),
        required = False
    )

    status = serializers.ChoiceField(
        [(e.value, e.label) for e in Ticket.TicketStatus.Problem],
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



class ProblemAddTicketModelSerializer(
    ProblemTicketModelSerializer,
):
    """Serializer for `Add` user

    Args:
        ProblemTicketModelSerializer (class): Model Serializer
    """


    category = serializers.PrimaryKeyRelatedField(
        read_only = True,
    )


    class Meta(ProblemTicketModelSerializer.Meta):

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



class ProblemChangeTicketModelSerializer(
    ProblemTicketModelSerializer,
):
    """Serializer for `Problem` user

    Args:
        ProblemTicketModelSerializer (class): Problem Model Serializer
    """


    category = serializers.PrimaryKeyRelatedField(
        read_only = True,
    )

    status = serializers.ChoiceField(
        [(e.value, e.label) for e in Ticket.TicketStatus.Problem],
        read_only = True,
    )


    class Meta(ProblemTicketModelSerializer.Meta):

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



class ProblemTriageTicketModelSerializer(
    ProblemTicketModelSerializer,
):
    """Serializer for `Triage` user

    Args:
        ProblemTicketModelSerializer (class): Problem Model Serializer
    """


    class Meta(ProblemTicketModelSerializer.Meta):

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



class ProblemImportTicketModelSerializer(
    ProblemTicketModelSerializer,
):
    """Serializer for `Import` user

    Args:
        ProblemTicketModelSerializer (class): Problem Model Serializer
    """

    class Meta(ProblemTicketModelSerializer.Meta):

        read_only_fields = [
            'id',
            'display_name',
            'status_badge',
            'ticket_type',
            '_urls',
        ]


    is_import: bool = True



class ProblemTicketViewSerializer(
    TicketViewSerializer,
    ProblemTicketModelSerializer,
):

    pass
