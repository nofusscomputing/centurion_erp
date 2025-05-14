from api.exceptions import UnknownTicketType
from api.viewsets.common import ModelViewSet

from access.models.tenant import Tenant as Organization

from assistance.serializers.request import (
    RequestAddTicketModelSerializer,
    RequestChangeTicketModelSerializer,
    RequestTriageTicketModelSerializer,
    RequestImportTicketModelSerializer,
    RequestTicketModelSerializer,
    RequestTicketViewSerializer
)

from core.serializers.ticket_depreciated import (
    Ticket,
)

from itim.serializers.change import (
    ChangeAddTicketModelSerializer,
    ChangeChangeTicketModelSerializer,
    ChangeImportTicketModelSerializer,
    ChangeTriageTicketModelSerializer,
    ChangeTicketModelSerializer,
    ChangeTicketViewSerializer,
)

from itim.serializers.incident import (
    IncidentAddTicketModelSerializer,
    IncidentChangeTicketModelSerializer,
    IncidentImportTicketModelSerializer,
    IncidentTriageTicketModelSerializer,
    IncidentTicketModelSerializer,
    IncidentTicketViewSerializer,
)

from itim.serializers.problem import (
    ProblemAddTicketModelSerializer,
    ProblemChangeTicketModelSerializer,
    ProblemImportTicketModelSerializer,
    ProblemTriageTicketModelSerializer,
    ProblemTicketModelSerializer,
    ProblemTicketViewSerializer,
)

from project_management.serializers.project_task import (
    ProjectTaskAddTicketModelSerializer,
    ProjectTaskChangeTicketModelSerializer,
    ProjectTaskImportTicketModelSerializer,
    ProjectTaskTriageTicketModelSerializer,
    ProjectTaskTicketModelSerializer,
    ProjectTaskTicketViewSerializer,
)

from settings.models.user_settings import UserSettings



class TicketViewSet(ModelViewSet):

    filterset_fields = [
        'category',
        'external_system',
        'impact',
        'milestone',
        'organization',
        'parent_ticket',
        'priority',
        'project',
        'status',
        'urgency',
    ]

    search_fields = [
        'title',
        'description',
    ]

    model = Ticket

    _ticket_type_id: int = None

    _ticket_type: str = None
    """Name for type of ticket

    String is Camel Cased.
    """


    def get_permission_required(self):

        organization = None

        if self._permission_required:

            return self._permission_required


        if(
            self.action == 'create'
            or self.action == 'partial_update'
            or self.action == 'update'
        ):

            if 'organization' in self.request.data:

                organization = Organization.objects.get(
                    pk = int(self.request.data['organization'])
                )

            elif(
                self.action == 'partial_update'
                or self.action == 'update'
            ):

                queryset = self.get_queryset()

                if len(queryset) > 0:

                    obj = queryset[0]

                    organization = obj.organization

        if self.action == 'create':

            action_keyword = 'add'

            if organization:

                if self.request.tenancy.has_organization_permission(
                    organization = organization,
                    permissions_required = str('core.import_ticket_' + self._ticket_type).lower().replace(' ', '_')
                ):

                    action_keyword = 'import'


        elif self.action == 'destroy':

            action_keyword = 'delete'

        elif self.action == 'list':

            action_keyword = 'view'

        elif self.action == 'partial_update':

            action_keyword = 'change'

            if organization:

                if self.request.tenancy.has_organization_permission(
                    organization = organization,
                    permissions_required = str('core.triage_ticket_' + self._ticket_type).lower().replace(' ', '_')
                ):

                    action_keyword = 'triage'


        elif self.action == 'retrieve':

            action_keyword = 'view'

        elif self.action == 'update':

            action_keyword = 'change'

            if self.request.tenancy.has_organization_permission(
                organization = organization,
                permissions_required = str('core.triage_ticket_' + self._ticket_type).lower().replace(' ', '_')
            ):

                action_keyword = 'triage'


        elif(
            self.action is None
            or self.action == 'metadata'
        ):

            action_keyword = 'view'

        else:

            raise ValueError('unable to determin the action_keyword')

        self._permission_required = str(
            'core.' + action_keyword + '_ticket_' + self._ticket_type).lower().replace(' ', '_'
        )

        return self._permission_required



    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        self.get_ticket_type()


        if self.kwargs.get('pk', None):

            queryset = self.model.objects.select_related(
                'organization',
                'category',
                'project',
                'milestone',
                'opened_by',
            ).prefetch_related(
                'assigned_teams',
                'assigned_users',
                'subscribed_teams',
                'subscribed_users',
            ).filter( pk = int( self.kwargs['pk'] ) )

        else:

            queryset = self.model.objects.select_related(
                'organization',
                'category',
                'project',
                'milestone',
                'opened_by',
            ).prefetch_related(
                'assigned_teams',
                'assigned_users',
                'subscribed_teams',
                'subscribed_users',
            )

        if str(self._ticket_type).lower().replace(' ', '_') == 'project_task':

            queryset = queryset.filter(
                project_id = int(self.kwargs['project_id'])
            )

        else:

            queryset = queryset.filter(
                ticket_type = self._ticket_type_id
            )


        self.queryset = queryset

        return self.queryset


    def get_ticket_type(self) -> None:

        ticket_type_id: int = None

        if self._ticket_type_id is None:

            ticket_types = [e for e in Ticket.TicketType]

            for i in range( 0, len(ticket_types) ):

                if self._ticket_type.lower() == str(ticket_types[i].label).lower():

                    ticket_type_id = int(ticket_types[i])

                    break

            self._ticket_type_id = ticket_type_id


        if self._ticket_type_id is None:

            raise UnknownTicketType()


    def get_serializer_class(self):

        serializer_prefix:str = None

        self.get_ticket_type()

        serializer_prefix = str(self._ticket_type).replace(' ', '')

        if (
            self.action == 'create'
            or self.action == 'list'
            or self.action == 'partial_update'
            or self.action == 'update'
        ):

            organization = self._obj_organization


            if organization:

                if (    # Must be first as the priority to pickup
                    self._ticket_type
                    and self.action != 'list'
                    and self.action != 'retrieve'
                ):


                    if self.request.tenancy.has_organization_permission(
                        organization = organization,
                        permissions_required = 'core.import_ticket_' + str(self._ticket_type).lower().replace(' ', '_')
                    ) and not self.request.user.is_superuser:

                        serializer_prefix = serializer_prefix + 'Import'

                    elif self.request.tenancy.has_organization_permission(
                        organization = organization,
                        permissions_required = 'core.triage_ticket_' + str(self._ticket_type).lower().replace(' ', '_')
                    ) or self.request.user.is_superuser:

                        serializer_prefix = serializer_prefix + 'Triage'

                    elif self.request.tenancy.has_organization_permission(
                        organization = organization,
                        permissions_required = 'core.change_ticket_' + str(self._ticket_type).lower().replace(' ', '_')
                    ):

                        serializer_prefix = serializer_prefix + 'Change'

                    elif self.request.tenancy.has_organization_permission(
                        organization = organization,
                        permissions_required = 'core.add_ticket_' + str(self._ticket_type).lower().replace(' ', '_')
                    ):

                        serializer_prefix = serializer_prefix + 'Add'

                    elif self.request.tenancy.has_organization_permission(
                        organization = organization,
                        permissions_required = 'core.view_ticket_' + str(self._ticket_type).lower().replace(' ', '_')
                    ):

                        serializer_prefix = serializer_prefix + 'View'


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[serializer_prefix + 'TicketViewSerializer']

        else:

            self.serializer_class = globals()[serializer_prefix + 'TicketModelSerializer']

        return self.serializer_class


    def get_view_serializer_name(self) -> str:
        """Get the Models `View` Serializer name.

        Override this function if required and/or the serializer names deviate from default.

        Returns:
            str: Models View Serializer Class name
        """

        if self.view_serializer_name is None:

            self.view_serializer_name = super().get_view_serializer_name()

            for remove_str in [ 'ChangeTicketView', 'AddTicketView', 'ImportTicketView', 'TriageTicketView' ]:

                self.view_serializer_name = self.view_serializer_name.replace(remove_str, 'TicketView')


        return self.view_serializer_name
