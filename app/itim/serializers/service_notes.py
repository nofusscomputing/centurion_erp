from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itim.models.service_notes import (
    ServiceNotes
)



class ServiceNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ServiceNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ServiceNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ServiceNoteViewSerializer(
    ModelNoteViewSerializer,
    ServiceNoteModelSerializer,
):

    pass