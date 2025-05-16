from rest_framework import serializers

from assistance.models.knowledge_base_notes import KnowledgeBaseNotes

from api.serializers import common

from centurion.serializers.user import UserBaseSerializer

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class KnowledgeBaseNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class KnowledgeBaseNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = KnowledgeBaseNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class KnowledgeBaseNoteViewSerializer(
    ModelNoteViewSerializer,
    KnowledgeBaseNoteModelSerializer,
):

    pass