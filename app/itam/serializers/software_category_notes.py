from core.serializers.model_notes import (
    ModelNoteBaseSerializer,
    ModelNoteModelSerializer,
    ModelNoteViewSerializer
)

from itam.models.software_category_notes import (
    SoftwareCategoryNotes
)



class SoftwareCategoryNoteBaseSerializer(ModelNoteBaseSerializer):

    pass


class SoftwareCategoryNoteModelSerializer(
    ModelNoteModelSerializer
):


    class Meta:

        model = SoftwareCategoryNotes

        fields =  ModelNoteModelSerializer.Meta.fields + [
            'model',
        ]

        read_only_fields = ModelNoteModelSerializer.Meta.read_only_fields + [
            'model',
            'content_type',
        ]



class SoftwareCategoryNoteViewSerializer(
    ModelNoteViewSerializer,
    SoftwareCategoryNoteModelSerializer,
):

    pass