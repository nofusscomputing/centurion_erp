from assistance.models.knowledge_base_category_notes import KnowledgeCategoryBaseNotes

from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class KnowledgeBaseCategoryNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class KnowledgeBaseCategoryNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = KnowledgeCategoryBaseNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class KnowledgeBaseCategoryNoteViewSerializer(
    ModelNoteViewSerializer,
    KnowledgeBaseCategoryNoteModelSerializer,
):

    pass