from rest_framework.reverse import reverse

from rest_framework import serializers

from access.models.tenant import Tenant

from centurion.serializers.user import UserBaseSerializer

from core import fields as centurion_field

Organization = Tenant


class TenantBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_tenant-detail", format="html"
    )

    class Meta:

        model = Tenant

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



class TenantModelSerializer(
    TenantBaseSerializer
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
            # 'notes': reverse(
            #     "v2:_api_v2_organization_note-list",
            #     request=self._context['view'].request,
            #     kwargs={
            #         'model_id': item.pk
            #     }
            # ),
            'teams': reverse("v2:_api_tenant_team-list", request=self._context['view'].request, kwargs={'organization_id': item.pk}),
        }

    model_notes = centurion_field.MarkdownField( required = False )

    class Meta:

        model = Tenant

        fields = '__all__'

        fields =  [
             'id',
            'display_name',
            'name',
            'model_notes',
            'manager',
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


class TenantViewSerializer(TenantModelSerializer):
    pass

    manager = UserBaseSerializer(many=False, read_only = True)
