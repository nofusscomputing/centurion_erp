from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from devops.models.feature_flag_notes import FeatureFlagNotes



class FeatureFlagNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class FeatureFlagNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = FeatureFlagNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class FeatureFlagNoteViewSerializer(
    ModelNoteViewSerializer,
    FeatureFlagNoteModelSerializer,
):

    pass