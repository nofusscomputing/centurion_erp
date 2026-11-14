import pytest



@pytest.fixture( scope = 'class')
def model(model_itasset):

    yield model_itasset


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itasset):

    request.cls.kwargs_create_item = kwargs_itasset()

    yield kwargs_itasset

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass


@pytest.fixture( scope = 'class')
def model_serializer(serializer_itasset):

    yield serializer_itasset
