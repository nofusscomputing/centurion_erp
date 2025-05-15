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
