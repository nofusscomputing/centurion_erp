from rest_framework import serializers

from access.serializers.organization import TenantBaseSerializer

from api.serializers import common

from core.models.ticket.ticket_comment_category import TicketCommentCategory



class TicketCommentCategoryBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.HyperlinkedIdentityField(
        view_name="v2:_api_ticketcommentcategory-detail", format="html"
    )


    class Meta:

        model = TicketCommentCategory

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


class TicketCommentCategoryModelSerializer(
    common.CommonModelSerializer,
    TicketCommentCategoryBaseSerializer
):


    _urls = serializers.SerializerMethodField('get_url')


    class Meta:

        model = TicketCommentCategory

        fields = '__all__'

        fields =  [
            'id',
            'organization',
            'display_name',
            'parent',
            'name',
            'model_notes',
            'comment',
            'notification',
            'solution',
            'task',
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


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if 'view' in self._context:

            if(
                (
                    self._context['view'].action == 'partial_update'
                    or self._context['view'].action == 'update'
                ) and getattr(self.instance, 'pk', None)
            ):

                self.fields['parent'].queryset = self.fields['parent'].queryset.exclude(
                    id=self.instance.pk
                )


    def validate(self, attrs):

        if self.instance:

            if 'parent' in attrs:

                if int(attrs['parent'].id) == self.instance.pk:

                    raise serializers.ValidationError(
                        detail = {
                            'parent': 'Cant set self as parent category'
                        },
                        code = 'parent_not_self'
                    )

        return attrs



class TicketCommentCategoryViewSerializer(TicketCommentCategoryModelSerializer):

    organization = TenantBaseSerializer( read_only = True )
