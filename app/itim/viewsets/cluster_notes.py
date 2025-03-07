from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itim.serializers.cluster_notes import (
    ClusterNotes,
    ClusterNoteModelSerializer,
    ClusterNoteViewSerializer
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Cluster',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ClusterNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Cluster note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Cluster notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Cluster note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Cluster note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ClusterNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ClusterNoteViewSerializer


        else:
            
            self.serializer_class = ClusterNoteModelSerializer

        return self.serializer_class
