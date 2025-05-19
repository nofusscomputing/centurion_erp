from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.operating_system_notes import (
    OperatingSystemNotes
)


class OperatingSystemNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class OperatingSystemNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = OperatingSystemNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class OperatingSystemNoteViewSerializer(
    ModelNoteViewSerializer,
    OperatingSystemNoteModelSerializer,
):

    pass