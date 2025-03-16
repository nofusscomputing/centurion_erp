from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from access.serializers.organization_notes import (
    OrganizationNotes,
    OrganizationNoteModelSerializer,
    OrganizationNoteViewSerializer,
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to an organization',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=OrganizationNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete an organization note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all organization notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single organization note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update an organization note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = OrganizationNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = OrganizationNoteViewSerializer


        else:
            
            self.serializer_class = OrganizationNoteModelSerializer

        return self.serializer_class
