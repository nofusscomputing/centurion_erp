import datetime
import pytest

from itim.models.clusters import Cluster



@pytest.fixture( scope = 'class')
def model_cluster():

    yield Cluster


@pytest.fixture( scope = 'class')
def kwargs_cluster(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'cluster_' + random_str,
    }

    yield kwargs.copy()
