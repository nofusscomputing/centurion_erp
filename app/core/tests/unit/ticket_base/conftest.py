import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketbase):

    request.cls.model = model_ticketbase

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketbase):

    request.cls.kwargs_create_item = kwargs_ticketbase.copy()

    yield kwargs_ticketbase.copy()


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketbase):

    yield serializer_ticketbase

