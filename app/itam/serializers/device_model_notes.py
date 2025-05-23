from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.device_model_notes import DeviceModelNotes



class DeviceModelNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class DeviceModelNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = DeviceModelNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class DeviceModelNoteViewSerializer(
    ModelNoteViewSerializer,
    DeviceModelNoteModelSerializer,
):

    pass