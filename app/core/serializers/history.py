from rest_framework.reverse import reverse
from rest_framework import serializers

from access.serializers.organization import OrganizationBaseSerializer

from app.serializers.user import UserBaseSerializer

from core.models.model_history import ModelHistory



class HistoryBaseSerializer(serializers.ModelSerializer):

    display_name = serializers.SerializerMethodField('get_display_name')

    def get_display_name(self, item) -> str:

        return str( item )

    url = serializers.SerializerMethodField('get_my_url')

    def get_my_url(self, item) -> str:

        return reverse("v2:_api_v2_model_history-detail", 
                request=self._context['view'].request,
                kwargs={
                    'model_class': self._kwargs['context']['view'].kwargs['model_class'],
                    'model_id': self._kwargs['context']['view'].kwargs['model_id'],
                    'pk': item.pk
                }
            )


    class Meta:

        model = ModelHistory

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


class HistoryModelSerializer(HistoryBaseSerializer):


    after = serializers.JSONField(read_only=True)

    before = serializers.JSONField(read_only=True)

    _urls = serializers.SerializerMethodField('get_url')

    def get_url(self, item) -> dict:

        return {
            '_self': reverse("v2:_api_v2_model_history-detail", 
                request=self._context['view'].request,
                kwargs={
                    'app_label': self._kwargs['context']['view'].kwargs['app_label'],
                    'model_name': self._kwargs['context']['view'].kwargs['model_name'],
                    'model_id': self._kwargs['context']['view'].kwargs['model_id'],
                    'pk': item.pk
                }
            ),
        }


    model = serializers.SerializerMethodField('get_model', label = 'device')

    def get_model(self, item):

        model = {}

        model = item.get_serialized_model_field( self.context )

        return model


    child_model = serializers.SerializerMethodField('get_child_model')

    def get_child_model(self, item):

        model = {}

        model = item.get_serialized_child_model_field( self.context )

        return model

    content = serializers.SerializerMethodField('get_content')

    def get_content(self, item):

        model = getattr(item, item.get_related_field_name( item ))

        content = model.model._meta.model_name

        if self.get_child_model(item):

            return getattr(model, item.get_related_field_name( model )).child_model._meta.model_name

        return content


    class Meta:

        model = ModelHistory

        fields =  [
             'id',
            'display_name',
            'content',
            'before',
            'after',
            'action',
            'user',
            'model',
            'child_model',
            'organization',
            'created',
            '_urls',
        ]

        read_only_fields = [
             'id',
            'display_name',
            'created',
            '_urls',
        ]



class HistoryViewSerializer(HistoryModelSerializer):

    organization = OrganizationBaseSerializer( read_only = True )

    user = UserBaseSerializer( read_only = True )
