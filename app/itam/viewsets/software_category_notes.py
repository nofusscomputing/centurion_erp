from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from itam.serializers.software_category_notes import (
    SoftwareCategoryNotes,
    SoftwareCategoryNoteModelSerializer,
    SoftwareCategoryNoteViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Software Category',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=SoftwareCategoryNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Software Category note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Software Category notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Software Category note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Software Category note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = SoftwareCategoryNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = SoftwareCategoryNoteViewSerializer


        else:
            
            self.serializer_class = SoftwareCategoryNoteModelSerializer

        return self.serializer_class
