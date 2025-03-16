from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itam.serializers.device_model_notes import (
    DeviceModelNotes,
    DeviceModelNoteModelSerializer,
    DeviceModelNoteViewSerializer,
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a device model',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=DeviceModelNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device model note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all device model notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device model note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device model note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = DeviceModelNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = DeviceModelNoteViewSerializer


        else:
            
            self.serializer_class = DeviceModelNoteModelSerializer

        return self.serializer_class
