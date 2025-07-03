from rest_framework.reverse import reverse

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from access.serializers.organization import TenantBaseSerializer
from access.serializers.teams import TeamBaseSerializer

from centurion.serializers.user import UserBaseSerializer

from api.serializers import common

from assistance.models.knowledge_base_category import KnowledgeBaseCategory



class KnowledgeBaseCategoryBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> str:

        return item.get_url( request = self.context['view'].request )


    class Meta:

        model = KnowledgeBaseCategory

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



class KnowledgeBaseCategoryModelSerializer(
    common.CommonModelSerializer,
    KnowledgeBaseCategoryBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        get_url.update({
            'organization': reverse(
                'v2:_api_organization-list',
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



    class Meta:

        model = KnowledgeBaseCategory

        fields = '__all__'

        fields =  [
            'id',
            'organization',
            'name',
            'display_name',
            'model_notes',
            'parent_category',
            'target_user',
            'target_team',
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


            if 'parent_category' in self.initial_data:

                if self.instance.id == self.initial_data['parent_category']:

                    raise ValidationError(
                        detail = {
                            'parent_category': 'Can not assign self as parent caategory'
                        },
                        code = 'parent_category_not_self'
                    )


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



class KnowledgeBaseCategoryViewSerializer(KnowledgeBaseCategoryModelSerializer):

    organization = TenantBaseSerializer( many=False, read_only=True )\
    
    parent_category = KnowledgeBaseCategoryBaseSerializer( many = False, read_only = True)

    target_team = TeamBaseSerializer( read_only = True, many = True)

    target_user = UserBaseSerializer( read_only = True )
