from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from devops.models.git_repository.gitlab_notes import GitLabRepositoryNotes



class GitLabRepositoryNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class GitLabRepositoryNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = GitLabRepositoryNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class GitLabRepositoryNoteViewSerializer(
    ModelNoteViewSerializer,
    GitLabRepositoryNoteModelSerializer,
):

    pass