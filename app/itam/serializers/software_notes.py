from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.software_notes import (
    SoftwareNotes
)



class SoftwareNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class SoftwareNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = SoftwareNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class SoftwareNoteViewSerializer(
    ModelNoteViewSerializer,
    SoftwareNoteModelSerializer,
):

    pass