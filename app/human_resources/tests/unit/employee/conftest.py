import pytest



@pytest.fixture( scope = 'class')
def model(model_employee):

    yield model_employee

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_employee):

    request.cls.kwargs_create_item = kwargs_employee.copy()

    yield kwargs_employee.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
