from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from devops.models.git_group_notes import GitGroupNotes



class GitGroupNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class GitGroupNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = GitGroupNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class GitGroupNoteViewSerializer(
    ModelNoteViewSerializer,
    GitGroupNoteModelSerializer,
):

    pass