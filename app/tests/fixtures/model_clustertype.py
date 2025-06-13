import datetime
import pytest

from itim.models.clusters import ClusterType



@pytest.fixture( scope = 'class')
def model_clustertype():

    yield ClusterType


@pytest.fixture( scope = 'class')
def kwargs_clustertype(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'clustertype_' + random_str,
    }

    yield kwargs.copy()
