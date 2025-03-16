from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.serializers.team_notes import (
    TeamNotes,
    TeamNoteModelSerializer,
    TeamNoteViewSerializer,
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Team',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=TeamNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a team note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all team notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single team note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a team note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = TeamNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = TeamNoteViewSerializer


        else:
            
            self.serializer_class = TeamNoteModelSerializer

        return self.serializer_class
