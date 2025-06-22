import datetime
import pytest

from itam.models.software import Software



@pytest.fixture( scope = 'class')
def model_software(request):

    yield Software


@pytest.fixture( scope = 'class')
def kwargs_software(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'software_' + random_str,
    }

    yield kwargs.copy()
