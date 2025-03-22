from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from devops.models.git_repository.base import GitRepository, GitGroup
from devops.serializers.git_group import BaseSerializer as GitGroupBaseSerializer


@extend_schema_serializer(component_name = 'GitBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:devops:_api_v2_git_repository-detail", format="html"
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


    class Meta:

        model = GitRepository

        fields = [
            'id',
            'display_name',
            'organization',
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

        default_read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'organization',
            'display_name',
            'organization',
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

    organization = OrganizationBaseSerializer( read_only = True )

    git_group = GitGroupBaseSerializer( read_only = True )
