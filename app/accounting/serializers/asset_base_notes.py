from accounting.models.asset_base_notes import AssetBaseNotes

from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)



class AssetBaseNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class AssetBaseNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = AssetBaseNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class AssetBaseNoteViewSerializer(
    ModelNoteViewSerializer,
    AssetBaseNoteModelSerializer,
):

    pass