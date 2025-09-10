import datetime
import pytest

from access.models.tenant import Tenant
from access.serializers.organization import (
    TenantBaseSerializer,
    TenantModelSerializer,
    TenantViewSerializer
)


@pytest.fixture( scope = 'class')
def model_tenant(clean_model_from_db):

    yield Tenant

    clean_model_from_db(Tenant)


@pytest.fixture( scope = 'class')
def kwargs_tenant( django_db_blocker, model_user ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        user = model_user.objects.create(
            username = 'a'+random_str,
            password = 'password'
        )

    kwargs = {
        'name': 'te',
        'manager': user,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        user.delete()


@pytest.fixture( scope = 'class')
def serializer_tenant():

    yield {
        'base': TenantBaseSerializer,
        'model': TenantModelSerializer,
        'view': TenantViewSerializer
    }
