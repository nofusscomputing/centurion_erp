import pytest

from datetime import datetime

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

    def factory():

        with django_db_blocker.unblock():

            user = model_user.objects.create(
                username = 'a' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
                password = 'password'
            )

        kwargs = {
            'name': 'te' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'manager': user,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_tenant():

    yield {
        'base': TenantBaseSerializer,
        'model': TenantModelSerializer,
        'view': TenantViewSerializer
    }
