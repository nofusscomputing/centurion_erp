import pytest

from devops.models.git_repository.base import (
    GitGroup,
    GitRepository,
)
from devops.serializers.git_repository.base import (
    ModelSerializer,
    ViewSerializer
)


@pytest.fixture( scope = 'class')
def model_gitrepository(request):

    yield GitRepository


@pytest.fixture( scope = 'class')
def serializer_gitrepository():

    yield {
        'model': ModelSerializer,
        'view': ViewSerializer,
    }


@pytest.fixture( scope = 'class')
def kwargs_gitrepository(django_db_blocker,
    kwargs_centurionmodel, model_gitgroup, kwargs_gitgroup
):

    kwargs = kwargs_gitgroup.copy()
    kwargs.update({
        'name': 'gitrepo'
    })

    with django_db_blocker.unblock():

        git_group = model_gitgroup.objects.create(
            **kwargs
        )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'provider': GitGroup.GitProvider.GITHUB,
        'provider_id': 1,
        'git_group': git_group,
        'path': 'a_path',
        'name': 'the name',
        'description': 'a random bit of text.',
        'modified': '2025-06-09T01:02:03Z'
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        try:
            git_group.delete()
        except:
            pass
