from assistance.models.knowledge_base_notes import KnowledgeBaseNotes

from core.serializers.model_notes import (
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