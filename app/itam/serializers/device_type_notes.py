from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.device_type_notes import (
    DeviceTypeNotes
)



class DeviceTypeNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class DeviceTypeNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = DeviceTypeNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class DeviceTypeNoteViewSerializer(
    ModelNoteViewSerializer,
    DeviceTypeNoteModelSerializer,
):

    pass