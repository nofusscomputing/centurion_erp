from rest_framework import serializers
from rest_framework.reverse import reverse

from drf_spectacular.utils import extend_schema_serializer

from access.functions.permissions import permission_queryset
from access.models.role import Role
from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from app.serializers.permission import PermissionBaseSerializer



@extend_schema_serializer(component_name = 'RoleBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = Role

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



@extend_schema_serializer(component_name = 'RoleModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """Role Base Model"""


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'tickets': reverse(
                "v2:_api_v2_item_tickets-list",
                request=self._context['view'].request,
                kwargs={
                    'item_class': self.Meta.model._meta.model_name,
                    'item_id': item.pk
                    }
            )
        })

        return get_url


    permissions = serializers.PrimaryKeyRelatedField(many = True, queryset=permission_queryset(), required = False)


    class Meta:

        model = Role

        fields = [
            'id',
            'organization',
            'display_name',
            'name',
            'permissions',
            'model_notes',
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



@extend_schema_serializer(component_name = 'RoleViewSerializer')
class ViewSerializer(ModelSerializer):
    """Role Base View Model"""

    organization = TenantBaseSerializer( many=False, read_only=True )

    permissions = PermissionBaseSerializer( many=True, read_only=True )
