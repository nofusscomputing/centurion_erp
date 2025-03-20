from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from api.serializers import common

from devops.models.git_group import GitGroup
from devops.models.git_repository.github import GitHubRepository
from devops.serializers.git_repository.base import (
    BaseSerializer,
    ViewSerializer as GitViewSerializer
)



class GroupField(serializers.PrimaryKeyRelatedField):


    def __init__(self, **kwargs):

        kwargs['label'] = GitHubRepository.git_group.field.verbose_name
        kwargs['help_text'] = GitHubRepository.git_group.field.help_text

        super().__init__(**kwargs)


    def get_queryset(self):

        qs = GitGroup.objects.filter(
            provider = int(GitGroup.GitProvider.GITHUB)
        )

        return qs



@extend_schema_serializer(component_name = 'GitHubModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """GitHub Repository"""

    _urls = serializers.SerializerMethodField('get_url')

    git_group = GroupField( required = True, write_only = True )

    class Meta:

        model = GitHubRepository

        # note_basename = 'devops:_api_v2_feature_flag_note'

        fields = '__all__'

        read_only_fields = [
            'id',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



@extend_schema_serializer(component_name = 'GitHubViewSerializer')
class ViewSerializer(
    ModelSerializer,
    GitViewSerializer
):
    """GitHub View Repository"""

    pass
