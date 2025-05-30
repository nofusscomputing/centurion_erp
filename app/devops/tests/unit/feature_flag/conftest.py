import pytest

from devops.models.feature_flag import FeatureFlag



@pytest.fixture( scope = 'class')
def model(request):

    yield FeatureFlag
