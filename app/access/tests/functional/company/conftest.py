import pytest

from access.models.company_base import Company



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Company

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from access.serializers.entity_company import ModelSerializer


    yield ModelSerializer
