import pytest

from devops.models.git_repository.github import (
    GitHubRepository,
)
from devops.serializers.git_repository.github import (
    ModelSerializer,
    ViewSerializer
)


@pytest.fixture( scope = 'class')
def model_githubrepository(request):

    yield GitHubRepository


@pytest.fixture( scope = 'class')
def serializer_githubrepository():

    yield {
        'model': ModelSerializer,
        'view': ViewSerializer,
    }


@pytest.fixture( scope = 'class')
def kwargs_githubrepository( kwargs_gitrepository ):

    kwargs = {
        **kwargs_gitrepository.copy(),
        'wiki': True,
        'issues': True,
        'sponsorships': True,
        'preserve_this_repository': True,
        'discussions': True,
        'projects': True,
    }

    yield kwargs.copy()
