import pytest

from devops.models.git_repository.github import (
    GitHubRepository,
)
from devops.serializers.git_repository.github import (
    ModelSerializer,
    ViewSerializer
)


@pytest.fixture( scope = 'class')
def model_githubrepository(clean_model_from_db):

    yield GitHubRepository

    clean_model_from_db(GitHubRepository)


@pytest.fixture( scope = 'class')
def serializer_githubrepository():

    yield {
        'model': ModelSerializer,
        'view': ViewSerializer,
    }


@pytest.fixture( scope = 'class')
def kwargs_githubrepository( kwargs_gitrepository ):

    def factory():

        kwargs = {
            **kwargs_gitrepository(),
            'wiki': True,
            'issues': True,
            'sponsorships': True,
            'preserve_this_repository': True,
            'discussions': True,
            'projects': True,
        }

        return kwargs

    yield factory
