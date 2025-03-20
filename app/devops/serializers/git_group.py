from drf_spectacular.utils import extend_schema_serializer

from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from api.serializers import common

from core import exceptions as centurion_exceptions

from devops.models.git_group import GitGroup


@extend_schema_serializer(component_name = 'GitGroupBaseSerializer')
class BaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:devops:_api_v2_feature_flag-detail", format="html"
    )


    class Meta:

        model = GitGroup

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

@extend_schema_serializer(component_name = 'GitGroupModelSerializer')
class ModelSerializer(
    common.CommonModelSerializer,
    BaseSerializer
):
    """Base Git Repository"""
    # _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = GitGroup

        # note_basename = 'devops:_api_v2_feature_flag_note'

        fields = '__all__'

        # fields =  [
        #     'id',
        #     'organization',
        #     'display_name',

        #     'name',
        #     'description',
        #     'enabled',
        #     'model_notes',
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


    def is_valid(self, raise_exceptions = False):

        is_valid = super().is_valid(raise_exceptions = raise_exceptions)

        if self.validated_data.get('parent_group', None):

            if self.validated_data['parent_group'].provider != self.validated_data['provider']:

                is_valid = False

                raise centurion_exceptions.ValidationError(
                    detail = {
                        'parent_group': 'GIT Providers between parent the the one selected must match'
                    },
                    code = 'parent_provider_must_match'
                )

        return is_valid



@extend_schema_serializer(component_name = 'GitGroupViewSerializer')
class ViewSerializer(ModelSerializer):

    organization = OrganizationBaseSerializer( read_only = True )
