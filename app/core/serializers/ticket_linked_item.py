from rest_framework.fields import empty
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from assistance.serializers.request import TicketBaseSerializer

from core.fields.badge import BadgeField
from core.models.ticket.ticket import Ticket
from core.models.ticket.ticket_linked_items import TicketLinkedItem



class TicketLinkedItemBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item):

        return str( item )


    url = serializers.SerializerMethodField('my_url')

    def my_url(self, item):

        return item.get_url( request = self._context['view'].request )


    created = serializers.DateTimeField( source = 'ticket.created', read_only = True )

    class Meta:

        model = TicketLinkedItem

        fields = [
            'id',
            'display_name',
            'created'
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'created'
            'url',
        ]


class TicketLinkedItemModelSerializer(TicketLinkedItemBaseSerializer):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item):

        return {
            '_self': item.get_url( request = self._context['view'].request )
        }


    class Meta:

        model = TicketLinkedItem

        fields = [
            'id',
            'display_name',
            'item',
            'item_type',
            'ticket',
            'organization',
            'created',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            # 'item',
            # 'item_type',
            'ticket',
            'organization',
            'created',
            '_urls',
        ]

    

    def is_valid(self, *, raise_exception=False):

        is_valid = super().is_valid( raise_exception = raise_exception )


        if 'view' in self._context:

            ticket = Ticket.objects.get(pk = int(self._context['view'].kwargs['ticket_id']) )

            self.validated_data['ticket'] = ticket

            self.validated_data['organization_id'] = ticket.organization.id


        return is_valid



class TicketLinkedItemViewSerializer(TicketLinkedItemModelSerializer):


    organization = OrganizationBaseSerializer(many=False, read_only=True)

    item = serializers.SerializerMethodField('get_item')

    def get_item(self, item) -> dict:

        base_serializer: dict = None

        if item.item_type == TicketLinkedItem.Modules.CLUSTER:

            from itim.serializers.cluster import Cluster, ClusterBaseSerializer

            base_serializer = ClusterBaseSerializer

            model = Cluster

        elif item.item_type == TicketLinkedItem.Modules.CONFIG_GROUP:

            from config_management.serializers.config_group import ConfigGroups, ConfigGroupBaseSerializer

            base_serializer = ConfigGroupBaseSerializer

            model = ConfigGroups

        elif item.item_type == TicketLinkedItem.Modules.DEVICE:

            from itam.serializers.device import Device, DeviceBaseSerializer

            base_serializer = DeviceBaseSerializer

            model = Device

        elif item.item_type == TicketLinkedItem.Modules.OPERATING_SYSTEM:

            from itam.serializers.operating_system import OperatingSystem, OperatingSystemBaseSerializer

            base_serializer = OperatingSystemBaseSerializer

            model = OperatingSystem

        elif item.item_type == TicketLinkedItem.Modules.SERVICE:

            from itim.serializers.service import Service, ServiceBaseSerializer

            base_serializer = ServiceBaseSerializer

            model = Service

        elif item.item_type == TicketLinkedItem.Modules.SOFTWARE:

            from itam.serializers.software import Software, SoftwareBaseSerializer

            base_serializer = SoftwareBaseSerializer

            model = Software

        
        if not base_serializer:

            return {
                'id': int(item.item)
            }

        
        try:

            model = model.objects.get(
                pk = int(item.item) 
            )

        except:

            return {}


        return base_serializer(
            model,
            context=self._context
        ).data

    ticket = TicketBaseSerializer(read_only = True)
