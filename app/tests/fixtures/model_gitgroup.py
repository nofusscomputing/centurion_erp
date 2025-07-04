import pytest

from devops.models.git_group import GitGroup
from devops.serializers.git_group import (
    ModelSerializer,
    ViewSerializer
)


@pytest.fixture( scope = 'class')
def model_gitgroup(request):

    yield GitGroup


@pytest.fixture( scope = 'class')
def serializer_gitgroup():

    yield {
        'model': ModelSerializer,
        'view': ViewSerializer,
    }


@pytest.fixture( scope = 'class')
def kwargs_gitgroup(kwargs_centurionmodel):

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'parent_group': None,
        'provider': GitGroup.GitProvider.GITHUB,
        'provider_pk': 1,
        'name': 'a name',
        'path': 'a_path',
        'description': 'a random bit of text.'
    }

    yield kwargs.copy()
