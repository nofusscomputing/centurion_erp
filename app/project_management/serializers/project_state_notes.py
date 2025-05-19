from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from project_management.models.project_state_notes import ProjectStateNotes



class ProjectStateNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ProjectStateNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ProjectStateNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ProjectStateNoteViewSerializer(
    ModelNoteViewSerializer,
    ProjectStateNoteModelSerializer,
):

    pass