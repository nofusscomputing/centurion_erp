import pytest
import random

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
                username = 'a' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
                password = 'password'
            )

        kwargs = {
            'name': 'te' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
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
