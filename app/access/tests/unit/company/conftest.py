import pytest



@pytest.fixture( scope = 'class')
def model(model_company):

    yield model_company



@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_company):

    request.cls.kwargs_create_item = kwargs_company.copy()

    yield kwargs_company.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
