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


@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_company):

    request.cls.kwargs_create_item = kwargs_company.copy()

    yield kwargs_company.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
