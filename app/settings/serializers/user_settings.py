from rest_framework.reverse import reverse

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from settings.models.user_settings import UserSettings



class UserSettingsBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_user_settings-detail", format="html"
    )

    class Meta:

        model = UserSettings

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



class UserSettingsModelSerializer(UserSettingsBaseSerializer):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': reverse("v2:_api_v2_user_settings-detail", request=self._context['view'].request, kwargs={'pk': item.pk}),
            'tokens': reverse(
                "v2:_api_v2_user_settings_token-list",
                request=self._context['view'].request,
                kwargs={
                    'model_id': item.user.pk
                }
            )
        }


    class Meta:

        model = UserSettings

        fields = '__all__'

        # fields =  [
        #     'id',
        #     'organization',
        #     'display_name',
        #     'name',
        #     'template',
        #     'colour',
        #     'cluster',
        #     'devices',
        #     'software',
        #     'model_notes',
        #     'created',
        #     'modified',
        #     '_urls',
        # ]

        read_only_fields = [
            'user',
        ]


class UserSettingsViewSerializer(UserSettingsModelSerializer):

    default_organization = TenantBaseSerializer( many = False, read_only = True )
