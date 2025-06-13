import pytest

from devops.models.git_repository.gitlab import (
    GitLabRepository,
)
from devops.serializers.git_repository.gitlab import (
    ModelSerializer,
    ViewSerializer
)


@pytest.fixture( scope = 'class')
def model_gitlabrepository(request):

    yield GitLabRepository


@pytest.fixture( scope = 'class')
def serializer_gitlabrepository():

    yield {
        'model': ModelSerializer,
        'view': ViewSerializer,
    }


@pytest.fixture( scope = 'class')
def kwargs_gitlabrepository( kwargs_gitrepository ):

    kwargs = {
        **kwargs_gitrepository.copy(),
        'visibility': True,
    }

    yield kwargs.copy()
