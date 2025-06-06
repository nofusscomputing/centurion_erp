from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from app.serializers.user import UserBaseSerializer

from api.serializers import common
from api.serializers.common import OrganizationField
from api.exceptions import UnknownTicketType

from core import exceptions as centurion_exception
from core import fields as centurion_field
from core.models.ticket.ticket import Ticket

from core.fields.badge import Badge, BadgeField
from core.serializers.ticket_category import TicketCategoryBaseSerializer

from project_management.serializers.project import ProjectBaseSerializer
from project_management.serializers.project_milestone import ProjectMilestoneBaseSerializer



class TicketBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = Ticket

        fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]

    is_import: bool = False


class TicketModelSerializer(
    common.CommonModelSerializer,
    TicketBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        ticket_type = str(item.get_ticket_type_display()).lower().replace(' ', '_')

        url_dict: dict = {
            '_self': item.get_url( request = self._context['view'].request ),
            'comments': reverse('v2:_api_v2_ticket_comment-list', request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
            'linked_items': reverse("v2:_api_v2_ticket_linked_item-list", request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
        }

        if item.project:

            url_dict.update({
                'project': reverse("v2:_api_v2_project-list", request=self._context['view'].request, kwargs={}),
            })

        if item.category:

            url_dict.update({
            'ticketcategory': reverse(
                'v2:_api_v2_ticket_category-list',
                request=self._context['view'].request,
                kwargs={},
            ) + '?' + ticket_type + '=true',
            })


        url_dict.update({
            'related_tickets': reverse("v2:_api_v2_ticket_related-list", request=self._context['view'].request, kwargs={'ticket_id': item.pk}),
        })


        return url_dict


    description = centurion_field.MarkdownField( required = True, style_class = 'large' )

    duration = serializers.IntegerField(source='duration_ticket', read_only=True)

    impact_badge = BadgeField(label='Impact')

    priority_badge = BadgeField(label='Priority')

    status_badge = BadgeField(label='Status')

    urgency_badge = BadgeField(label='Urgency')

    organization = OrganizationField( required = True, write_only = True )


    class Meta:
        """Ticket Model Base Meta

        This class specifically has only `id` in fields and all remaining fields
        as ready only so as to prevent using this serializer directly. The intent
        is that for each ticket type there is a seperate serializer for that ticket
        type.

        These serializers are for items that are common for ALL tickets.
        """

        model = Ticket

        fields = [
            'id',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'assigned_teams',
            'assigned_users',
            'category',
            'created',
            'modified',
            'status',
            'status_badge',
            'parent_ticket',
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



    def validate_field_organization(self) -> bool:
        """Check `organization field`

        Raises:
            ValidationError: user tried to change the organization

        Returns:
            True (bool): OK
            False (bool): User tried to edit the organization
        """

        is_valid: bool = True

        if self.instance is not None:

            if self.instance.pk is not None:

                if 'organization' in self.initial_data:

                        is_valid = False

                        raise centurion_exception.ValidationError(
                            detail = 'cant edit field: organization',
                            code = 'cant_edit_field_organization',
                        )

        elif self.instance is None:

            if 'organization' not in self.initial_data:

                is_valid = False

                raise centurion_exception.ValidationError(
                    detail = {
                        'organization': 'this field is required'
                    },
                    code = 'required',
                )


        return is_valid


    def validate_field_milestone( self ) -> bool:

        is_valid: bool = False

        if self.instance is not None:

            if self.instance.milestone is None:

                return True

            else:

                if self.instance.project is None:

                    raise centurion_exception.ValidationError(
                        details = 'Milestones require a project',
                        code = 'milestone_requires_project',
                    )

                    return False

                if self.instance.project.id == self.instance.milestone.project.id:

                    return True

                else:

                    raise centurion_exception.ValidationError(
                        detail = 'Milestone must be from the same project',
                        code = 'milestone_same_project',
                    )

        return is_valid


    def validate(self, data):

        if 'view' in self._context:

            if str(self._context['view']._ticket_type).lower().replace(' ', '_') == 'project_task':

                data['project_id'] = int(self._context['view'].kwargs['project_id'])

            if self._context['view'].action == 'create':

                if hasattr(self._context['view'], 'request'):

                    if self.is_import:

                        if data['opened_by'] is None:

                            raise centurion_exception.ValidationError(
                                detail = {
                                    'opened_by': 'Opened by user is required'
                                },
                                code = 'required',
                            )


                    else:

                        data['opened_by_id'] = self._context['view'].request.user.id


            if hasattr(self._context['view'], '_ticket_type_id'):

                data['ticket_type'] = self._context['view']._ticket_type_id

            else:

                raise UnknownTicketType()


            if self.instance is None:

                subscribed_users: list = []

                if 'subscribed_users' in data:

                    subscribed_users: list = data['subscribed_users']

                if self.is_import:

                    data['subscribed_users'] = subscribed_users + [ data['opened_by'].id ]

                else:

                    data['subscribed_users'] = subscribed_users + [ data['opened_by_id'] ]


                data['status'] = int(Ticket.TicketStatus.All.NEW)


        if(
            data.get('parent_ticket', None)
            and (
                self._context['view'].action == 'partial_update'
                or self._context['view'].action == 'update'
            )
        ):

            if not data['parent_ticket'].circular_dependency_check(
                ticket = self.instance,
                parent = data['parent_ticket']
            ):

                raise centurion_exception.ValidationError(
                    detail = {
                        'parent_ticket': 'Adding this ticket will create a circular dependency'
                    },
                    code = 'no_parent_circular_dependency',
                )



        self.validate_field_organization()

        self.validate_field_milestone()

        return data


class TicketViewSerializer(TicketModelSerializer):

    assigned_teams = TeamBaseSerializer(many=True)

    assigned_users = UserBaseSerializer(many=True, label='Assigned Users')

    category = TicketCategoryBaseSerializer()

    parent_ticket = TicketBaseSerializer()

    opened_by = UserBaseSerializer()

    organization = TenantBaseSerializer(many=False, read_only=True)

    project = ProjectBaseSerializer(many=False, read_only=True)

    milestone = ProjectMilestoneBaseSerializer(many=False, read_only=True)

    subscribed_teams = TeamBaseSerializer(many=True)

    subscribed_users = UserBaseSerializer(many=True)
