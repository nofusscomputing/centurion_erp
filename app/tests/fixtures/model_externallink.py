import datetime
import pytest

from settings.models.external_link import ExternalLink

@pytest.fixture( scope = 'class')
def model_externallink():

    yield ExternalLink


@pytest.fixture( scope = 'class')
def kwargs_externallink( kwargs_centurionmodel ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'el' + random_str,
        'button_text': 'bt' + random_str,
        'template': 'boo'
    }

    yield kwargs.copy()
