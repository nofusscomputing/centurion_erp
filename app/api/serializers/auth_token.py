import datetime
import re

from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.models.tokens import AuthToken
from api.serializers import common

from core import exceptions as centurion_exception



class AuthTokenBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_v2_cluster-detail",
    )

    class Meta:

        model = AuthToken

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


class AuthTokenModelSerializer(
    common.CommonModelSerializer,
    AuthTokenBaseSerializer
):

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        get_url = super().get_url( item = item )

        # del get_url['history']
        del get_url['knowledge_base']


        return get_url


    expires = serializers.DateTimeField(
        initial = (datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=90)).replace(microsecond=0).isoformat(),
        )

    token = serializers.CharField(initial=AuthToken().generate, write_only = True )


    class Meta:

        model = AuthToken

        fields =  [
            'id',
            'display_name',
            'note',
            'token',
            'user',
            'expires',
            'created',
            'modified',
            '_urls',
        ]

        read_only_fields = [
            'id',
            'display_name',
            'user',
            'created',
            'modified',
            '_urls',
        ]


    def validate(self, attrs):

        if self.context['request'].user.id != int(self.context['view'].kwargs['model_id']):

            raise centurion_exception.PermissionDenied()


        if not self.Meta.model().validate_note_no_token(attrs['note'], attrs['token']):

            raise centurion_exception.ValidationError(
                detail = {
                    "note": "No more than nine chars of token can be contained within the notes field"
                },
                code = 'note_no_contain_token'
            )


        if not re.fullmatch(r'[0-9|a-f]{64}', str(attrs['token']).lower()):


            raise centurion_exception.ValidationError(
                detail = {
                    "token": "Token appears to have been edited."
                },
                code = 'token_not_sha256'
            )


        attrs['token'] = self.Meta.model().token_hash(attrs['token'])

        attrs = super().validate(attrs)

        attrs['user'] = self.context['request'].user

        return attrs



class AuthTokenViewSerializer(AuthTokenModelSerializer):

    organization = TenantBaseSerializer( many = False, read_only = True )
