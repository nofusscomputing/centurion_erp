from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from accounting.serializers.asset_base_notes import (
    AssetBaseNotes,
    AssetBaseNoteModelSerializer,
    AssetBaseNoteViewSerializer,
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to an Asset',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=AssetBaseNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an Asset note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Asset notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Asset note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an Asset note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = AssetBaseNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = AssetBaseNoteViewSerializer


        else:
            
            self.serializer_class = AssetBaseNoteModelSerializer

        return self.serializer_class
