import datetime
import pytest

from itam.models.software import SoftwareCategory



@pytest.fixture( scope = 'class')
def model_softwarecategory(request):

    yield SoftwareCategory


@pytest.fixture( scope = 'class')
def kwargs_softwarecategory(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'sc_' + random_str,
    }

    yield kwargs.copy()
