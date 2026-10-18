import pytest



@pytest.fixture( scope = 'class')
def model(model_itassetoperatingsystem):

    yield model_itassetoperatingsystem


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_itassetoperatingsystem):

    request.cls.kwargs_create_item = kwargs_itassetoperatingsystem()

    yield kwargs_itassetoperatingsystem

    if hasattr(request.cls, 'kwargs_create_item'):
        try:
            del request.cls.kwargs_create_item
        except:
            pass


@pytest.fixture( scope = 'class')
def model_serializer(serializer_itassetoperatingsystem):

    yield serializer_itassetoperatingsystem
