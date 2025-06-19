import datetime
import pytest

from access.models.contact import Contact



@pytest.fixture( scope = 'class')
def model_contact():

    yield Contact


@pytest.fixture( scope = 'class')
def kwargs_contact( kwargs_person ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_person.copy(),
        'entity_type': 'contact',
        'email': 'p' + random_str + '@domain.tld'
    }

    yield kwargs.copy()
