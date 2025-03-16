from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from core.viewsets.model_notes import ModelNoteViewSet

from project_management.serializers.project_milestone_notes import (
    ProjectMilestoneNotes,
    ProjectMilestoneNoteModelSerializer,
    ProjectMilestoneNoteViewSerializer,
)




@extend_schema_view(
    create=extend_schema(
        summary = 'Add a note to a Project Milestone',
        description = '',
        responses = {
            201: OpenApiResponse(description='created', response=ProjectMilestoneNoteViewSerializer),
            400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing create permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a Project Milestone note',
        description = ''
    ),
    list = extend_schema(
        summary = 'Fetch all Project Milestone notes',
        description='',
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single Project Milestone note',
        description='',
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update a Project Milestone note',
        description = ''
    ),
)
class ViewSet(ModelNoteViewSet):

    model = ProjectMilestoneNotes


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = ProjectMilestoneNoteViewSerializer


        else:
            
            self.serializer_class = ProjectMilestoneNoteModelSerializer

        return self.serializer_class
