from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from devops.models.git_repository.github_notes import GitHubRepositoryNotes



class GitHubRepositoryNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class GitHubRepositoryNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = GitHubRepositoryNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class GitHubRepositoryNoteViewSerializer(
    ModelNoteViewSerializer,
    GitHubRepositoryNoteModelSerializer,
):

    pass