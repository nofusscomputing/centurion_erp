from core.models.ticket.ticket_comment_category_notes import TicketCommentCategoryNotes

from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class TicketCommentCategoryNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class TicketCommentCategoryNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = TicketCommentCategoryNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class TicketCommentCategoryNoteViewSerializer(
    ModelNoteViewSerializer,
    TicketCommentCategoryNoteModelSerializer,
):

    pass