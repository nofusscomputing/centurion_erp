
from centurion.serializers.user import UserBaseSerializer

from core.serializers.model_notes import (
    ModelNotes,
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from settings.models.external_link_notes import (
    ExternalLinkNotes
)


class ExternalLinkNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ExternalLinkNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ExternalLinkNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ExternalLinkNoteViewSerializer(
    ModelNoteViewSerializer,
    ExternalLinkNoteModelSerializer,
):

    pass