import pytest



@pytest.fixture( scope = 'class')
def model(request, model_slmticket):

    request.cls.model = model_slmticket

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_slmticket):

    request.cls.kwargs_create_item = kwargs_slmticket.copy()

    yield kwargs_slmticket.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_slmticket):

    yield serializer_slmticket

