import pytest

# from itam.models import ITAsset



@pytest.fixture( scope = 'class')
def model(request, model_itassetsoftware):

    request.cls.model = model_itassetsoftware

    yield model_itassetsoftware

    del request.cls.model


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



@pytest.fixture(scope='function')
def create_serializer(serializer_itassetsoftware):

    yield serializer_itassetsoftware['create']
