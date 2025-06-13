import datetime
import pytest

from itim.models.services import Service



@pytest.fixture( scope = 'class')
def model_service():

    yield Service


@pytest.fixture( scope = 'class')
def kwargs_service(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'service_' + random_str,
    }

    yield kwargs.copy()
