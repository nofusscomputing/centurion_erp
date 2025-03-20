from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from core import exceptions as centurion_exceptions

from devops.models.git_group import GitGroup
from devops.models.git_repository.gitlab import GitLabRepository
from devops.serializers.git_repository.base import (
    BaseSerializer,
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

# @extend_schema_serializer(component_name = 'GitLabModelSerializer')
# class BaseSerializer(serializers.ModelSerializer):

#     display_name = serializers.SerializerMethodField('get_display_name')

#     def get_display_name(self, item) -> str:

#         return str( item )

#     url = serializers.HyperlinkedIdentityField(
#         view_name="v2:devops:_api_v2_feature_flag-detail", format="html"
#     )


#     class Meta:

#         model = GitLabRepository

#         fields = [
#             'id',
#             'display_name',
#             'url',
#         ]

#         read_only_fields = [
#             'id',
#             'display_name',
#             'url',
#         ]

@extend_schema_serializer(component_name = 'GitLabModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """GitLab Repository"""
    # _urls = serializers.SerializerMethodField('get_url')

    git_group = GroupField( required = True, write_only = True )


    class Meta:

        model = GitLabRepository

        # note_basename = 'devops:_api_v2_feature_flag_note'

        fields = '__all__'

        # fields =  [
        #     'id',
        #     'organization',
        #     # 'display_name',
        #     'name',
        #     # 'description',
        #     # 'enabled',
        #     # 'model_notes',
        #     'created',
        #     'modified',
        #     '_urls',
        # ]

        # read_only_fields = [
        #     'id',
        #     'display_name',
        #     'created',
        #     'modified',
        #     '_urls',
        # ]



@extend_schema_serializer(component_name = 'GitLabViewSerializer')
class ViewSerializer(
    ModelSerializer,
    GitViewSerializer
):
    """GitLab View Repository"""

    # git_group = GroupField( read_only = True )
    pass
