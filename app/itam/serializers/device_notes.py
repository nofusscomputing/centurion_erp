from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.device_notes import (
    DeviceNotes
)



class DeviceNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class DeviceNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = DeviceNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class DeviceNoteViewSerializer(
    ModelNoteViewSerializer,
    DeviceNoteModelSerializer,
):

    pass