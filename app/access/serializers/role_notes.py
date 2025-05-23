from access.models.role_notes import RoleNotes

from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class RoleNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class RoleNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = RoleNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class RoleNoteViewSerializer(
    ModelNoteViewSerializer,
    RoleNoteModelSerializer,
):

    pass