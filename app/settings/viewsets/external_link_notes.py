from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from settings.serializers.external_links_notes import (
    ExternalLinkNotes,
    ExternalLinkNoteModelSerializer,
    ExternalLinkNoteViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a External Link',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ExternalLinkNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a External Link note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all External Link notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single External Link note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a External Link note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ExternalLinkNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ExternalLinkNoteViewSerializer


        else:
            
            self.serializer_class = ExternalLinkNoteModelSerializer

        return self.serializer_class
