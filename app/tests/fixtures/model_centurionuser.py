import pytest

from datetime import datetime

from access.models.centurion_user import CenturionUser



@pytest.fixture( scope = 'class')
def model_centurionuser(clean_model_from_db):

    yield CenturionUser

    clean_model_from_db(CenturionUser)


@pytest.fixture( scope = 'class')
def kwargs_centurionuser():

    def factory():

        kwargs = {}

        kwargs = {
            'username': "test_user-" + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'password': "password"
        }

        return kwargs

    yield factory
