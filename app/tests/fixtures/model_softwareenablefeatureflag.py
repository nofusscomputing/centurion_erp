import pytest

from devops.models.software_enable_feature_flag import SoftwareEnableFeatureFlag



@pytest.fixture( scope = 'class')
def model_softwareenablefeatureflag(request):

    yield SoftwareEnableFeatureFlag
