from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itim.models.cluster_type_notes import (
    ClusterTypeNotes
)



class ClusterTypeNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ClusterTypeNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ClusterTypeNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ClusterTypeNoteViewSerializer(
    ModelNoteViewSerializer,
    ClusterTypeNoteModelSerializer,
):

    pass