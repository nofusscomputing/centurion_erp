import pytest

from human_resources.models.employee import Employee



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Employee

    yield request.cls.model

    del request.cls.model



@pytest.fixture(scope='function')
def create_serializer():

    from human_resources.serializers.entity_employee import ModelSerializer


    yield ModelSerializer


@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_employee):

    request.cls.kwargs_create_item = kwargs_employee.copy()

    yield kwargs_employee.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
