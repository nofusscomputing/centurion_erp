import pytest



@pytest.fixture( scope = 'class')
def model(model_employee):

    yield model_employee

@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_employee):

    request.cls.kwargs_create_item = kwargs_employee()

    yield kwargs_employee

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
