from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.serializers.entity_notes import (
    EntityNotes,
    EntityNoteModelSerializer,
    EntityNoteViewSerializer
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to an Entity',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=EntityNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Entity note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Entity notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Entity note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Entity note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = EntityNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = EntityNoteViewSerializer


        else:
            
            self.serializer_class = EntityNoteModelSerializer

        return self.serializer_class
