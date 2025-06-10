import datetime
import pytest

from devops.models.check_ins import CheckIn



@pytest.fixture( scope = 'class')
def model_checkin():

    yield CheckIn


@pytest.fixture( scope = 'class')
def kwargs_checkin(django_db_blocker,
    kwargs_centurionmodel, kwargs_featureflag
):

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'software': kwargs_featureflag['software'],
        'version': '1.20.300',
        'deployment_id': 'rand deploymentid',
        'feature': 'a feature',
    }

    yield kwargs.copy()
