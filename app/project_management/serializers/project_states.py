from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from assistance.serializers.knowledge_base import KnowledgeBaseBaseSerializer

from project_management.models.project_states import ProjectState



class ProjectStateBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_projectstate-detail", format="html"
    )


    class Meta:

        model = ProjectState

        fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'url',
        ]



class ProjectStateModelSerializer(
    common.CommonModelSerializer,
    ProjectStateBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = ProjectState

        fields =  [
            'id',
            'organization',
            'display_name',
            'name',
            'model_notes',
            'runbook',
            'is_completed',
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



class ProjectStateViewSerializer(ProjectStateModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

    runbook = KnowledgeBaseBaseSerializer( many = False, read_only = True )
