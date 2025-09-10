import datetime
import pytest

from access.models.centurion_user import CenturionUser



@pytest.fixture( scope = 'class')
def model_centurionuser(clean_model_from_db):

    yield CenturionUser

    clean_model_from_db(CenturionUser)


@pytest.fixture( scope = 'class')
def kwargs_centurionuser():

    kwargs = {}

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        'username': "test_user-" + random_str,
        'password': "password"
    }

    yield kwargs.copy()
