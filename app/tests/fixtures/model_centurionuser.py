import pytest
import random

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
            'username': "test_user-" + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'password': "password"
        }

        return kwargs

    yield factory
