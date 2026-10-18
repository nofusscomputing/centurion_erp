import pytest



@pytest.fixture( scope = 'class')
def model(model_itassetsoftware):

    yield model_itassetsoftware


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetsoftware):

    request.cls.kwargs_create_item = kwargs_itassetsoftware()

    yield kwargs_itassetsoftware

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass


@pytest.fixture( scope = 'class')
def model_serializer(serializer_itassetsoftware):

    yield serializer_itassetsoftware
