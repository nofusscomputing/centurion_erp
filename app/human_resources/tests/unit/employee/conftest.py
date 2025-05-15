import pytest

from human_resources.models.employee import Employee



@pytest.fixture( scope = 'class')
def model(request):

    request.cls.model = Employee

    yield request.cls.model

    del request.cls.model
