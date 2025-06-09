from rest_framework.reverse import reverse

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    PolymorphicProxySerializer,
)

# THis import only exists so that the migrations can be created
from devops.models.git_repository.github_history import GitHubHistory    # pylint: disable=W0611:unused-import
from devops.models.git_repository.gitlab_history import GitlabHistory    # pylint: disable=W0611:unused-import
from devops.models.git_group import GitGroup
from devops.serializers.git_repository.base import (    # pylint: disable=W0611:unused-import
    GitRepository,
    ModelSerializer,
    ViewSerializer,
)
from devops.serializers.git_repository.github import (
    GitHubRepository,
    ModelSerializer as GitHubModelSerializer,
    ViewSerializer as GitHubViewSerializer,
)
from devops.serializers.git_repository.gitlab import (
    GitLabRepository,
    ModelSerializer as GitLabModelSerializer,
    ViewSerializer as GitLabViewSerializer,
)

from api.viewsets.common import ModelViewSet




@extend_schema_view(
    create=extend_schema(
        parameters = [
            OpenApiParameter(
                name = 'git_provider',
                description = 'Select the provider the repository belongs to.',
                location = OpenApiParameter.PATH,
                required = True,
                allow_blank = False,
                type = str,
                enum = ['github', 'gitlab'],
            ),
        ],
        summary = 'Create a GIT Repository',
        description='Create',
        request = PolymorphicProxySerializer(
            component_name = 'Git Provider',
            serializers=[
                GitHubModelSerializer,
                GitLabModelSerializer,
            ],
            resource_type_field_name=None,
            many = False,
        ),
        responses = {
            201: OpenApiResponse(
                description='Created. Will be serialized with the serializer matching the provider.',
                response=PolymorphicProxySerializer(
                    component_name = 'Git Provider',
                    serializers=[
                        GitHubViewSerializer,
                        GitLabViewSerializer,
                    ],
                    resource_type_field_name=None,
                    many = False,
                ),
            ),
            403: OpenApiResponse(description='User is missing add permissions'),
        }
    ),
    destroy = extend_schema(
        parameters = [
            OpenApiParameter(
                name = 'git_provider',
                description = 'Select the provider the repository belongs to.',
                location = OpenApiParameter.PATH,
                required = True,
                allow_blank = False,
                type = str,
                enum = ['github', 'gitlab'],
            ),
        ],
        summary = 'Delete a GIT Repository',
        description = 'Delete',
        responses = {
            204: OpenApiResponse(description=''),
            403: OpenApiResponse(description='User is missing delete permissions'),
        }
    ),
    list = extend_schema(
        parameters = [
            OpenApiParameter(
                name = 'git_provider',
                description = 'Select the provider the repository belongs to.',
                location = OpenApiParameter.PATH,
                required = True,
                allow_blank = False,
                type = str,
                enum = ['github', 'gitlab'],
            ),
        ],
        summary = 'Fetch all GIT Repository',
        description='Fetch',
        responses = {
            200: OpenApiResponse(description='Will be serialized with the serializer matching the provider.',
                response=PolymorphicProxySerializer(
                    component_name = 'Git Provider',
                    serializers=[
                        GitHubViewSerializer,
                        GitLabViewSerializer,
                    ],
                    resource_type_field_name=None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    retrieve = extend_schema(
        parameters = [
            OpenApiParameter(
                name = 'git_provider',
                description = 'Select the provider the repository belongs to.',
                location = OpenApiParameter.PATH,
                required = True,
                allow_blank = False,
                type = str,
                enum = ['github', 'gitlab'],
            ),
        ],
        summary = 'Fetch a single GIT Repository',
        description='Fetch',
        responses = {
            200: OpenApiResponse(description='Will be serialized with the serializer matching the provider.',
                response=PolymorphicProxySerializer(
                    component_name = 'Git Provider',
                    serializers=[
                        GitHubViewSerializer,
                        GitLabViewSerializer,
                    ],
                    resource_type_field_name=None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing view permissions'),
        }
    ),
    update = extend_schema(exclude = True),
    partial_update = extend_schema(
        parameters = [
            OpenApiParameter(
                name = 'git_provider',
                description = 'Select the provider the repository belongs to.',
                location = OpenApiParameter.PATH,
                required = True,
                allow_blank = False,
                type = str,
                enum = ['github', 'gitlab'],
            ),
        ],
        summary = 'Update a GIT Repository',
        description = 'Update',
        responses = {
            200: OpenApiResponse(description='Will be serialized with the serializer matching the provider.',
                response=PolymorphicProxySerializer(
                    component_name = 'Git Provider',
                    serializers=[
                        GitHubViewSerializer,
                        GitLabViewSerializer,
                    ],
                    resource_type_field_name=None,
                    many = False,
                )
            ),
            403: OpenApiResponse(description='User is missing change permissions'),
        }
    ),
)
class ViewSet(ModelViewSet):
    """fdgdfgdf"""

    filterset_fields = [
        'organization',
        'provider',
    ]

    search_fields = [
        'description',
        'name',
        'provider_id',
    ]

    model = GitRepository

    view_description: str = 'GIT Repositories'


    def get_back_url(self) -> str:


        return reverse('v2:devops:_api_gitrepository-list', request = self.request )


    def get_page_layout(self):

        if len(self.page_layout) < 1:

            if hasattr(self, 'model'):

                if self.kwargs.get('pk', None):

                    model = getattr(self.queryset[0], self.kwargs['git_provider'] + 'repository')

                    self.page_layout = model.get_page_layout()

        return self.page_layout


    def get_queryset(self):

        if self.queryset is not None:

            return self.queryset

        
        if self.kwargs.get('git_provider', '') == 'github':

            self.queryset = GitHubRepository.objects.select_related(
                'git_group',
                ).all()

        elif self.kwargs.get('git_provider', '') == 'gitlab':

            self.queryset = GitLabRepository.objects.select_related(
                'git_group',
                ).all()

        else:

            self.queryset = self.model.objects.select_related(
                'git_group',
                'githubrepository',
                'gitlabrepository',
                ).all()

        if 'pk' in self.kwargs:

            if self.kwargs['pk']:

                self.queryset = self.queryset.filter( pk = int( self.kwargs['pk'] ) )


        return self.queryset

    
    def get_return_url(self) -> str:

        if 'pk' in self.kwargs:

            return self.queryset[0].get_url( request = self.request )

        return None


    def get_serializer_class(self):

        prefix: str = ''

        if self.kwargs.get('git_provider', '') == 'github':

            prefix = 'GitHub'

        elif self.kwargs.get('git_provider', '') == 'gitlab':

            prefix = 'GitLab'


        if (
            self.action == 'list'
            or self.action == 'retrieve'
        ):

            return globals()[prefix + 'ViewSerializer']

        else:

            return globals()[prefix + 'ModelSerializer']
