from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from access.serializers.organization import TenantBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from centurion.serializers.user import UserBaseSerializer

from api.serializers import common

from assistance.models.knowledge_base import KnowledgeBase
from assistance.serializers.knowledge_base_category import KnowledgeBaseCategoryBaseSerializer

from core import fields as centurion_field



class KnowledgeBaseBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = KnowledgeBase

        fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'title',
            'url',
        ]



class KnowledgeBaseModelSerializer(
    common.CommonModelSerializer,
    KnowledgeBaseBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        del get_url['knowledge_base']

        get_url.update({
            'category': reverse(
                'v2:_api_v2_knowledge_base_category-list',
                request=self.context['view'].request,
            ),
            'organization': reverse(
                'v2:_api_v2_organization-list',
                request=self.context['view'].request,
            ),
            'team': reverse(
                'v2:_api_v2_organization_team-list',
                request=self.context['view'].request,
                kwargs={
                    'organization_id': item.organization.id,
                }
            ),
            'user': reverse(
                'v2:_api_v2_user-list',
                request=self.context['view'].request,
            )
        })

        return get_url



    content = centurion_field.MarkdownField( required = False, style_class = 'large' )

    summary = centurion_field.MarkdownField( required = False, style_class = 'large' )


    class Meta:

        model = KnowledgeBase

        fields =  [
            'id',
            'organization',
            'category',
            'display_name',
            'title',
            'summary',
            'content',
            'release_date',
            'expiry_date',
            'target_user',
            'target_team',
            'responsible_user',
            'responsible_teams',
            'public',
            'is_global',
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


    def validate(self, attrs):

        target_team = None
        target_user = None


        if self.instance:

            if len(self.instance.target_team.filter()) > 0:

                target_team = self.instance.target_team.filter()[0]


            if hasattr(self.instance, 'target_user_id'):

                target_user = self.instance.target_user_id


        if 'target_team' in self.initial_data:

            target_team = self.initial_data['target_team']


        if 'target_user' in self.initial_data:

            target_user = self.initial_data['target_user']


        if target_team and target_user:

            raise ValidationError(
                detail = [
                    'Both a Target Team or Target User Cant be assigned at the same time. Use one or the other'
                ],
                code = 'invalid_not_both_target_team_user'
            )


        if not target_team and not target_user:

            raise ValidationError(
                detail = [
                    'A Target Team or Target User must be assigned.'
                ],
                code='invalid_need_target_team_or_user'
            )

        return super().validate(attrs)



class KnowledgeBaseViewSerializer(KnowledgeBaseModelSerializer):

    category = KnowledgeBaseCategoryBaseSerializer( read_only = True )

    organization = TenantBaseSerializer( many=False, read_only=True )

    responsible_teams = TeamBaseSerializer( read_only = True, many = True)

    responsible_user = UserBaseSerializer( read_only = True )

    target_team = TeamBaseSerializer( read_only = True, many = True)

    target_user = UserBaseSerializer( read_only = True )
