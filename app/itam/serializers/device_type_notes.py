from centurion.serializers.user import UserBaseSerializer

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.device_type_notes import (
    DeviceTypeNotes
)
from itam.serializers.device import DeviceBaseSerializer



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