from access.models.team_notes import TeamNotes

from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class TeamNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class TeamNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = TeamNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class TeamNoteViewSerializer(
    ModelNoteViewSerializer,
    TeamNoteModelSerializer,
):

    pass