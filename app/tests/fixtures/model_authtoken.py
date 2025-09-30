import datetime
import pytest
import random

from dateutil.relativedelta import relativedelta

from api.models.tokens import AuthToken
from api.serializers.auth_token import (
    AuthTokenBaseSerializer,
    AuthTokenModelSerializer,
    AuthTokenViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_authtoken(clean_model_from_db):

    yield AuthToken

    clean_model_from_db(AuthToken)


@pytest.fixture( scope = 'class')
def kwargs_authtoken(django_db_blocker,
    model_authtoken, model_user, kwargs_user
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_user()
            kwargs['username'] = 'at_' + str(random.randint(9999,99999))

            user = model_user.objects.create( **kwargs )

        kwargs = {
            'note': 'a note',
            'token': model_authtoken().generate,
            'user': user,
            'expires': (datetime.datetime.now() + relativedelta(months=1)).isoformat(timespec='seconds') + 'Z'
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_authtoken():

    yield {
        'base': AuthTokenBaseSerializer,
        'model': AuthTokenModelSerializer,
        'view': AuthTokenViewSerializer
    }
