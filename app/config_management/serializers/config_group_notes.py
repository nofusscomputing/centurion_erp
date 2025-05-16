from rest_framework import serializers

from api.serializers import common

from centurion.serializers.user import UserBaseSerializer

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from config_management.models.config_group_notes import ConfigGroupNotes



class ConfigGroupNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ConfigGroupNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ConfigGroupNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ConfigGroupNoteViewSerializer(
    ModelNoteViewSerializer,
    ConfigGroupNoteModelSerializer,
):

    pass