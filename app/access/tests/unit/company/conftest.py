import pytest



@pytest.fixture( scope = 'class')
def model(model_company):

    yield model_company



@pytest.fixture( scope = 'class')
def model_kwargs(request, kwargs_company):

    request.cls.kwargs_create_item = kwargs_company()

    yield kwargs_company

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_company):

    yield serializer_company
