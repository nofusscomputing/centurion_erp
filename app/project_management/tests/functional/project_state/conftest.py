import pytest



@pytest.fixture( scope = 'class')
def model(model_projectstate):

    yield model_projectstate


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_projectstate):

    request.cls.kwargs_create_item = kwargs_projectstate()

    yield kwargs_projectstate

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_projectstate):

    yield serializer_projectstate
