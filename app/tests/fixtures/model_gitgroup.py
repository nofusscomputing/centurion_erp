import pytest

from devops.models.git_group import GitGroup



@pytest.fixture( scope = 'class')
def model_gitgroup(request):

    yield GitGroup


@pytest.fixture( scope = 'class')
def kwargs_gitgroup(kwargs_centurionmodel):

    # kwargs = kwargs_centurionmodel.copy()
    # del kwargs['model_notes']

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
