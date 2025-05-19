from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from project_management.models.project_milestone_notes import ProjectMilestoneNotes



class ProjectMilestoneNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ProjectMilestoneNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ProjectMilestoneNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ProjectMilestoneNoteViewSerializer(
    ModelNoteViewSerializer,
    ProjectMilestoneNoteModelSerializer,
):

    pass