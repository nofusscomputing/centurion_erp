from functools import reduce

from operator import or_

from django.db import models

from rest_framework import serializers
from rest_framework.exceptions import ParseError

from drf_spectacular.utils import extend_schema_serializer

from access.functions.permissions import permission_queryset
from access.models.role import Role
from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from centurion.serializers.group import GroupBaseSerializer
from centurion.serializers.permission import PermissionBaseSerializer
from centurion.serializers.user import UserBaseSerializer



@extend_schema_serializer(component_name = 'RoleBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url()


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


    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )


        return get_url


    permissions = serializers.PrimaryKeyRelatedField(
        many = True, queryset=permission_queryset(), required = False
    )


    class Meta:

        model = Role

        fields = [
            'id',
            'organization',
            'display_name',
            'name',
            'permissions',
            'users',
            'groups',
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



    def to_internal_value(self, data):
        """Convert Permission Names

        Permission may be added in format `<app>.<permission>_<model>` this
        function converts to the permission pk.
        """

        if(
            'permissions' in data
            and isinstance(data['permissions'][0], str)
        ):

            filters = [
                models.Q(
                    content_type__app_label=app, codename=codename
                ) for app, codename in (
                    perm.split(".", 1) for perm in data['permissions']
                )
            ]

            PermissionModel = self.Meta.model.permissions.field.related_model

            permissions_id = [
                permission.id for permission in PermissionModel.objects.filter(
                    reduce(or_, filters)
                )
            ]


            if len(permissions_id) != len(data['permissions']):
                raise ParseError(
                    detail = 'A Permission was supplied that could not be found',
                    code = 'supplied_permission_does_not_exist'
                )

            data['permissions'] = permissions_id

        return super().to_internal_value(data)



@extend_schema_serializer(component_name = 'RoleViewSerializer')
class ViewSerializer(ModelSerializer):
    """Role Base View Model"""

    groups = GroupBaseSerializer( many=True, read_only=True )

    organization = TenantBaseSerializer( many=False, read_only=True )

    permissions = PermissionBaseSerializer( many=True, read_only=True )

    users = UserBaseSerializer( many=True, read_only=True )
