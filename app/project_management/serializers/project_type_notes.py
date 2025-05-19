from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from project_management.models.project_type_notes import ProjectTypeNotes



class ProjectTypeNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ProjectTypeNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ProjectTypeNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ProjectTypeNoteViewSerializer(
    ModelNoteViewSerializer,
    ProjectTypeNoteModelSerializer,
):

    pass