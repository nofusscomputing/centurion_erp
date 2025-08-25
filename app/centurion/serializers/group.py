from django.contrib.auth.models import Group

from rest_framework import serializers

from centurion.serializers.permission import PermissionBaseSerializer



class GroupBaseSerializer(serializers.ModelSerializer):


    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )


    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_group-detail", format="html"
    )

    permissions = PermissionBaseSerializer( many=True, read_only=True )


    class Meta:

        model = Group

        fields = [
            'id',
            'display_name',
            'name',
            'permissions',
            'url'
        ]

        read_only_fields = [
            'id',
            'display_name',
            'url'
        ]
