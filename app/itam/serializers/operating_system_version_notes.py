
from centurion.serializers.user import UserBaseSerializer

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.operating_system_version_notes import (
    OperatingSystemVersionNotes
)


class OperatingSystemVersionNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class OperatingSystemVersionNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = OperatingSystemVersionNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class OperatingSystemVersionNoteViewSerializer(
    ModelNoteViewSerializer,
    OperatingSystemVersionNoteModelSerializer,
):

    pass