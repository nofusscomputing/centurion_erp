import pytest



@pytest.fixture( scope = 'class')
def model(model_itassetmodel):

    yield model_itassetmodel


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetmodel):

    request.cls.kwargs_create_item = kwargs_itassetmodel()

    yield kwargs_itassetmodel

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item



@pytest.fixture( scope = 'class')
def model_serializer(serializer_itassetmodel):

    yield serializer_itassetmodel
