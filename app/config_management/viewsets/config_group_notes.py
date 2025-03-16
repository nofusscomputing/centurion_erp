from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from config_management.serializers.config_group_notes import (
    ConfigGroupNotes,
    ConfigGroupNoteModelSerializer,
    ConfigGroupNoteViewSerializer
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a config group',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ConfigGroupNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a config group note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all config group notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single config group note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a config group note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ConfigGroupNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ConfigGroupNoteViewSerializer


        else:
            
            self.serializer_class = ConfigGroupNoteModelSerializer

        return self.serializer_class
