import pytest

# from itam.models import ITAsset



@pytest.fixture( scope = 'class')
def model(request, model_itassetoperatingsystem):

    request.cls.model = model_itassetoperatingsystem

    yield model_itassetoperatingsystem

    del request.cls.model


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



@pytest.fixture(scope='function')
def create_serializer(serializer_itassetoperatingsystem):

    yield serializer_itassetoperatingsystem['create']
