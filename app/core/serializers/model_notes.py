from django.contrib.auth.models import ContentType
from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from app.serializers.user import UserBaseSerializer

from core.models.model_notes import ModelNotes



class ModelNoteBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_device-detail", format="html"
    )

    class Meta:

        model = ModelNotes

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



class ModelNoteModelSerializer(
    common.CommonModelSerializer,
    ModelNoteBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': item.get_url( request = self._context['view'].request ),
        }


    class Meta:

        model = ModelNotes

        fields =  [
             'id',
            'organization',
            'display_name',
            'content',
            'created_by',
            'modified_by',
            'content_type',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'organization',
            'created_by',
            'modified_by',
            'content_type',
            'created',
            'modified',
            '_urls',
        ]


    def validate(self, attrs):

        is_valid = False

        if (
            self._context['view'].action == 'partial_update'
            or self._context['view'].action == 'update'
        ):

            attrs['modified_by'] = self._context['request'].user

        else:

            related_model = self.fields.fields['model'].context['view'].model.model.field.related_model

            attrs['model_id'] = int(self.fields.fields['model'].context['view'].kwargs['model_id'])

            if str(related_model._meta.model_name).lower() == 'tenant':

                attrs['organization'] = related_model.objects.get(
                    pk = int(self.fields.fields['model'].context['view'].kwargs['model_id'])
                )
            elif self.fields.fields.get('organization', None):

                attrs['organization'] = related_model.objects.get(
                    pk = int(self.fields.fields['model'].context['view'].kwargs['model_id'])
                ).organization

            

            attrs['content_type'] = ContentType.objects.filter(
                app_label = related_model._meta.app_label,
                model = related_model._meta.model_name
            )[0]

            attrs['created_by'] = self._context['request'].user


        is_valid = super().validate(attrs)

        return is_valid


    def is_valid(self, *, raise_exception=False) -> bool:

        is_valid = super().is_valid(raise_exception=raise_exception)

        return is_valid



class ModelNoteViewSerializer(ModelNoteModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )

    created_by = UserBaseSerializer( many = False, read_only = True )

    modified_by = UserBaseSerializer( many = False, read_only = True )
