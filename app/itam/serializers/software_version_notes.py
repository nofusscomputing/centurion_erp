from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.software_version_notes import (
    SoftwareVersionNotes
)



class SoftwareVersionNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class SoftwareVersionNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = SoftwareVersionNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class SoftwareVersionNoteViewSerializer(
    ModelNoteViewSerializer,
    SoftwareVersionNoteModelSerializer,
):

    pass