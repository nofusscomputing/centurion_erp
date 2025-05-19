from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itim.models.cluster_notes import (
    ClusterNotes
)



class ClusterNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ClusterNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ClusterNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ClusterNoteViewSerializer(
    ModelNoteViewSerializer,
    ClusterNoteModelSerializer,
):

    pass