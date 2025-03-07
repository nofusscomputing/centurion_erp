from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itam.serializers.device_notes import (
    DeviceNotes,
    DeviceNoteModelSerializer,
    DeviceNoteViewSerializer
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a device',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=DeviceNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all device notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = DeviceNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = DeviceNoteViewSerializer


        else:
            
            self.serializer_class = DeviceNoteModelSerializer

        return self.serializer_class
