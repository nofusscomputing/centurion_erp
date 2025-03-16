from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.serializers.manufacturer_notes import (
    ManufacturerNotes,
    ManufacturerNoteModelSerializer,
    ManufacturerNoteViewSerializer,
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Manufacturer',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ManufacturerNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Manufacturer note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Manufacturer notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Manufacturer note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Manufacturer note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ManufacturerNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ManufacturerNoteViewSerializer


        else:
            
            self.serializer_class = ManufacturerNoteModelSerializer

        return self.serializer_class
