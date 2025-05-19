from core.models.manufacturer_notes import ManufacturerNotes

from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class ManufacturerNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class ManufacturerNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = ManufacturerNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class ManufacturerNoteViewSerializer(
    ModelNoteViewSerializer,
    ManufacturerNoteModelSerializer,
):

    pass