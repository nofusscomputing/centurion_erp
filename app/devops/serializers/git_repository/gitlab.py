from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core import exceptions as centurion_exceptions

from devops.models.git_group import GitGroup
from devops.models.git_repository.gitlab import GitLabRepository
from devops.serializers.git_repository.base import (
    BaseSerializer,
    ModelSerializer as GitModelSerializer,
    ViewSerializer as GitViewSerializer
)



class GroupField(serializers.PrimaryKeyRelatedField):


    def __init__(self, **kwargs):

        kwargs['label'] = GitLabRepository.git_group.field.verbose_name
        kwargs['help_text'] = GitLabRepository.git_group.field.help_text

        super().__init__(**kwargs)


    def get_queryset(self):

        qs = GitGroup.objects.filter(
            provider = int(GitGroup.GitProvider.GITLAB)
        )

        return qs



@extend_schema_serializer(component_name = 'GitLabModelSerializer')
class ModelSerializer(
    GitModelSerializer,
):
    """GitLab Repository"""

    git_group = GroupField( required = True, write_only = True )


    class Meta:

        model = GitLabRepository

        # note_basename = 'devops:_api_v2_feature_flag_note'

        fields = GitModelSerializer.Meta.fields + [
            'visibility',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = GitModelSerializer.Meta.default_read_only_fields + [
            'provider',
        ]


    def is_valid(self, raise_exception = False):

        is_valid = super().is_valid( raise_exception = raise_exception )

        self.validated_data['provider'] = getattr(
            GitGroup.GitProvider,
            str(self.context['view'].kwargs['git_provider']).upper()
        )

        return is_valid



@extend_schema_serializer(component_name = 'GitLabViewSerializer')
class ViewSerializer(
    GitViewSerializer,
    ModelSerializer,
):
    """GitLab View Repository"""

    pass
