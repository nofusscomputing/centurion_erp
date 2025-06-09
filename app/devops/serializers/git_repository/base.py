from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.fields.badge import BadgeField

from devops.models.git_repository.base import GitRepository
from devops.serializers.git_group import BaseSerializer as GitGroupBaseSerializer


@extend_schema_serializer(component_name = 'GitBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:devops:_api_gitrepository-detail", format="html"
    )


    class Meta:

        model = GitRepository

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

@extend_schema_serializer(component_name = 'GitModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """Base Git Repository"""
    _urls = serializers.SerializerMethodField('get_url')

    organization = serializers.PrimaryKeyRelatedField( read_only = True)

    provider_badge = BadgeField(label='Provider')

    class Meta:

        model = GitRepository

        fields = [
            'id',
            'display_name',
            'organization',
            'provider',
            'provider_badge',
            'provider_id',
            'git_group',
            'path',
            'name',
            'description',
            'model_notes',
            'created',
            'modified',
            '_urls',
        ]

        default_read_only_fields = [
            'id',
            'display_name',
            'provider_id',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'organization',
            'display_name',
            'provider',
            'provider_id',
            'git_group',
            'path',
            'name',
            'description',
            'model_notes',
            'created',
            'modified',
            '_urls',
        ]


    def is_valid(self, raise_exception = False):

        is_valid = super().is_valid( raise_exception = raise_exception )

        return is_valid



@extend_schema_serializer(component_name = 'GitViewSerializer')
class ViewSerializer(ModelSerializer):

    organization = TenantBaseSerializer( read_only = True )

    git_group = GitGroupBaseSerializer( read_only = True )
