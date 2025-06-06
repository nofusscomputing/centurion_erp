from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

from api.viewsets.common import ModelViewSet

from config_management.serializers.config_group import (    # pylint: disable=W0611:unused-import
    ConfigGroups,
    ConfigGroupModelSerializer,
    ConfigGroupViewSerializer
)



@extend_schema_view(
    create=extend_schema(
        summary = 'Create a config group',
        description='',
        responses = {
            # 200: OpenApiResponse(description='Allready exists', response=ConfigGroupViewSerializer),
            201: OpenApiResponse(description='Created', response=ConfigGroupViewSerializer),
            # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        summary = 'Delete a config group',
        description = '',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        summary = 'Fetch all config groups',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ConfigGroupViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        summary = 'Fetch a single config group',
        description='',
        responses = {
            200: OpenApiResponse(description='', response=ConfigGroupViewSerializer),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        summary = 'Update aconfig group',
        description = '',
        responses = {
            200: OpenApiResponse(description='', response=ConfigGroupViewSerializer),
            # 201: OpenApiResponse(description='Created', response=OrganizationViewSerializer),
            # # 400: OpenApiResponse(description='Validation failed.'),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet( ModelViewSet ):

    filterset_fields = [
        'organization',
        'parent',
    ]

    search_fields = [
        'name',
        'config',
    ]

    model = ConfigGroups

    view_description = 'Information Management Knowledge Base Article(s)'


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        if 'parent_group' in self.kwargs:

            self.queryset = super().get_queryset().filter(parent = self.kwargs['parent_group'])

        elif 'pk' in self.kwargs:

            self.queryset = super().get_queryset().filter( pk = self.kwargs['pk'] )

        else:

            self.queryset = super().get_queryset().filter( parent = None )
        
        return self.queryset


    def get_serializer_class(self):

        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ViewSerializer']

        else:

            self.serializer_class = globals()[str( self.model._meta.verbose_name).replace(' ' , '') + 'ModelSerializer']


        return self.serializer_class

