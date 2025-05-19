from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itim.models.port_notes import (
    PortNotes
)



class PortNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class PortNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = PortNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class PortNoteViewSerializer(
    ModelNoteViewSerializer,
    PortNoteModelSerializer,
):

    pass