from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itim.serializers.cluster_type_notes import (
    ClusterTypeNotes,
    ClusterTypeNoteModelSerializer,
    ClusterTypeNoteViewSerializer
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Cluster Type',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ClusterTypeNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Cluster Type note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Cluster Type notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Cluster Type note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Cluster Type note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ClusterTypeNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ClusterTypeNoteViewSerializer


        else:
            
            self.serializer_class = ClusterTypeNoteModelSerializer

        return self.serializer_class
