import pytest



@pytest.fixture( scope = 'class')
def model(model_operatingsystem):

    yield model_operatingsystem


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_operatingsystem):

    request.cls.kwargs_create_item = kwargs_operatingsystem.copy()

    yield kwargs_operatingsystem.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_device):

    yield serializer_device
