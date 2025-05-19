from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from project_management.models.project_notes import ProjectNotes



class ProjectNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ProjectNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ProjectNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ProjectNoteViewSerializer(
    ModelNoteViewSerializer,
    ProjectNoteModelSerializer,
):

    pass