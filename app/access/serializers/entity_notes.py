from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from access.models.entity_notes import EntityNotes



class EntityNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class EntityNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = EntityNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class EntityNoteViewSerializer(
    ModelNoteViewSerializer,
    EntityNoteModelSerializer,
):

    pass