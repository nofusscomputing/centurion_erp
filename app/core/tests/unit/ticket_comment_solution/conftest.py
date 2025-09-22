import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommentsolution):

    request.cls.model = model_ticketcommentsolution

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentsolution):

    request.cls.kwargs_create_item = kwargs_ticketcommentsolution.copy()

    yield kwargs_ticketcommentsolution.copy()


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommentsolution):

    yield serializer_ticketcommentsolution
