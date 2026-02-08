import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommenttask):

    request.cls.model = model_ticketcommenttask

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommenttask):

    request.cls.kwargs_create_item = kwargs_ticketcommenttask()

    yield kwargs_ticketcommenttask


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommenttask):

    yield serializer_ticketcommenttask
