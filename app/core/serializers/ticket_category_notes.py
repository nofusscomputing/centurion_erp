from core.models.ticket.ticket_category_notes import TicketCategoryNotes

from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class TicketCategoryNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class TicketCategoryNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = TicketCategoryNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class TicketCategoryNoteViewSerializer(
    ModelNoteViewSerializer,
    TicketCategoryNoteModelSerializer,
):

    pass