import pytest

from devops.models.feature_flag import FeatureFlag



@pytest.fixture( scope = 'class')
def model_featureflag(request):

    yield FeatureFlag


@pytest.fixture( scope = 'class')
def kwargs_featureflag(kwargs_centurionmodel):

    # kwargs = kwargs_centurionmodel.copy()
    # del kwargs['model_notes']

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'software': None,
        'name': 'a name',
        'description': ' a description',
        'enabled': True,
    }

    yield kwargs.copy()
