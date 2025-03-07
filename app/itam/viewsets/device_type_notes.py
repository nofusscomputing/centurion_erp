from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itam.serializers.device_type_notes import (
    DeviceTypeNotes,
    DeviceTypeNoteModelSerializer,
    DeviceTypeNoteViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a device type',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=DeviceTypeNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a device type note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all device type notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single device type note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a device type note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = DeviceTypeNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = DeviceTypeNoteViewSerializer


        else:
            
            self.serializer_class = DeviceTypeNoteModelSerializer

        return self.serializer_class
