import datetime
import pytest
import random

from api.models.tokens import AuthToken



@pytest.fixture( scope = 'class')
def model_authtoken():

    yield AuthToken


@pytest.fixture( scope = 'class')
def kwargs_authtoken(django_db_blocker,
    model_authtoken, model_user, kwargs_user
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        kwargs = kwargs_user.copy()
        kwargs['username'] = 'at_' + str(random.randint(9999,99999))

        user = model_user.objects.create( **kwargs )

    kwargs = {
        'note': 'a note',
        'token': model_authtoken().generate,
        'user': user,
        'expires': '2025-02-25T23:14Z'
    }

    yield kwargs

    with django_db_blocker.unblock():

        user.delete()
