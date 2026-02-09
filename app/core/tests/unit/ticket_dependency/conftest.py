import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketdependency):

    request.cls.model = model_ticketdependency

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketdependency):

    request.cls.kwargs_create_item = kwargs_ticketdependency()

    yield kwargs_ticketdependency


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketdependency):

    yield serializer_ticketdependency

