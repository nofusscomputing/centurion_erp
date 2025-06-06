from rest_framework import serializers
from rest_framework.reverse import reverse

from access.serializers.organization import Organization, TenantBaseSerializer

from api.serializers import common
from app.serializers.user import UserBaseSerializer

from access.serializers.teams import TeamBaseSerializer

from core import fields as centurion_field

from project_management.models.projects import Project
from project_management.serializers.project_states import ProjectStateBaseSerializer
from project_management.serializers.project_type import ProjectTypeBaseSerializer



class ProjectBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_project-detail", format="html"
    )

    class Meta:

        model = Project

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



class ProjectModelSerializer(
    common.CommonModelSerializer,
    ProjectBaseSerializer,
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'milestone': reverse("v2:_api_v2_project_milestone-list", request=self._context['view'].request, kwargs={'project_id': item.pk}),
            'tickets': reverse(
                "v2:_api_v2_ticket_project_task-list",
                request=self._context['view'].request,
                kwargs={
                    'project_id': item.pk
                }
            ),
        })

        return get_url


    description = centurion_field.MarkdownField( required = False, style_class = 'large' )
    completed = serializers.CharField( source = 'percent_completed', read_only = True )

    class Meta:

        model = Project

        fields =  [
            'id',
            'external_ref',
            'external_system',
            'organization',
            'display_name',
            'name',
            'description',
            'priority',
            'state',
            'estimation_project',
            'duration_project',
            'completed',
            'project_type',
            'code',
            'planned_start_date',
            'planned_finish_date',
            'real_start_date',
            'real_finish_date',
            'manager_user',
            'manager_team',
            'team_members',
            'is_deleted',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'estimation_project',
            'duration_project',
            'completed',
            'display_name',
            'external_ref',
            'external_system',
            'created',
            'modified',
            '_urls',
        ]



class ProjectImportSerializer(ProjectModelSerializer):


    class Meta(ProjectModelSerializer.Meta):


        read_only_fields = [
            'id',
            'completed',
            'display_name',
            'created',
            'modified',
            '_urls',
        ]



class ProjectViewSerializer(ProjectModelSerializer):

    manager_team = TeamBaseSerializer( many = False, read_only = True )

    manager_user = UserBaseSerializer( many = False, read_only = True )

    organization = TenantBaseSerializer( many = False, read_only = True )

    state = ProjectStateBaseSerializer( many = False, read_only = True )

    team_members = UserBaseSerializer( many = True, read_only = True )

    project_type = ProjectTypeBaseSerializer( many = False, read_only = True )
