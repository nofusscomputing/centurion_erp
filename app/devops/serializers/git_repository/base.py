from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from devops.models.git_repository.base import GitRepository
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

        fields = '__all__'

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]




@extend_schema_serializer(component_name = 'GitViewSerializer')
class ViewSerializer(ModelSerializer):

    organization = OrganizationBaseSerializer( read_only = True )

    git_group = GitGroupBaseSerializer( read_only = True )
