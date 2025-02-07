from rest_framework import serializers

from access.models import OrganizationNotes

from api.serializers import common

from app.serializers.user import UserBaseSerializer

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class OrganizationNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class OrganizationNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = OrganizationNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class OrganizationNoteViewSerializer(
    ModelNoteViewSerializer,
    OrganizationNoteModelSerializer,
):

    pass