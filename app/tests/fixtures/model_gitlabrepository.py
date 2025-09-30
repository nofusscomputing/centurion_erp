import pytest

from devops.models.git_repository.gitlab import (
    GitLabRepository,
)
from devops.serializers.git_repository.gitlab import (
    ModelSerializer,
    ViewSerializer
)


@pytest.fixture( scope = 'class')
def model_gitlabrepository(clean_model_from_db):

    yield GitLabRepository

    clean_model_from_db(GitLabRepository)


@pytest.fixture( scope = 'class')
def serializer_gitlabrepository():

    yield {
        'model': ModelSerializer,
        'view': ViewSerializer,
    }


@pytest.fixture( scope = 'class')
def kwargs_gitlabrepository( kwargs_gitrepository ):

    def factory():

        kwargs = {
            **kwargs_gitrepository(),
            'visibility': True,
        }

        return kwargs

    yield factory
