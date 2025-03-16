from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from assistance.serializers.knowledge_base_category_notes import (
    KnowledgeCategoryBaseNotes,
    KnowledgeBaseCategoryNoteModelSerializer,
    KnowledgeBaseCategoryNoteViewSerializer
)

from core.viewsets.model_notes import ModelNoteViewSet



@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a knowledge base Category',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=KnowledgeBaseCategoryNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a knowledge base Category note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all knowledge base Category notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single knowledge base Category note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a knowledge base Category note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = KnowledgeCategoryBaseNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = KnowledgeBaseCategoryNoteViewSerializer


        else:
            
            self.serializer_class = KnowledgeBaseCategoryNoteModelSerializer

        return self.serializer_class
