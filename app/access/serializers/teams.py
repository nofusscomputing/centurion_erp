from rest_framework.reverse import reverse

from rest_framework import serializers

from access.models import Team

from api.serializers import common

from access.functions.permissions import permission_queryset
from access.serializers.organization import OrganizationBaseSerializer

from app.serializers.permission import Permission, PermissionBaseSerializer

from core import fields as centurion_field



class TeamBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = Team

        fields = [
            'id',
            'display_name',
            'team_name',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'team_name',
            'url',
        ]



class TeamModelSerializer(
    common.CommonModelSerializer,
    TeamBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
            'knowledge_base': reverse(
                "v2:_api_v2_model_kb-list",
                request=self._context['view'].request,
                kwargs={
                    'model': self.Meta.model._meta.model_name,
                    'model_pk': item.pk
                }
            ),
            'notes': reverse(
                "v2:_api_v2_organization_team_note-list",
                request=self._context['view'].request,
                kwargs={
                    'organization_id': item.organization.pk,
                    'model_id': item.pk
                }
            ),
            'users': reverse(
                'v2:_api_v2_organization_team_user-list',
                request=self.context['view'].request,
                kwargs={
                    'organization_id': item.organization.id,
                    'team_id': item.pk
                }
            )
        }

    team_name = centurion_field.CharField( autolink = True )

    permissions = serializers.PrimaryKeyRelatedField(many = True, queryset=permission_queryset(), required = False)

    class Meta:

        model = Team

        fields = '__all__'

        fields =  [
             'id',
            'display_name',
            'team_name',
            'model_notes',
            'permissions',
            'organization',
            'is_global',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'name',
            'organization',
            'created',
            'modified',
            '_urls',
        ]



    def is_valid(self, *, raise_exception=True) -> bool:

        is_valid = False

        is_valid = super().is_valid(raise_exception=raise_exception)

        self.validated_data['organization_id'] = int(self._context['view'].kwargs['organization_id'])


        return is_valid



class TeamViewSerializer(TeamModelSerializer):

    organization = OrganizationBaseSerializer(many=False, read_only=True)

    permissions = PermissionBaseSerializer(many = True)
