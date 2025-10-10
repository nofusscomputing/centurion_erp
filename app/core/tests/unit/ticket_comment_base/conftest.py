import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommentbase):

    request.cls.model = model_ticketcommentbase

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentbase):

    request.cls.kwargs_create_item = kwargs_ticketcommentbase()

    yield kwargs_ticketcommentbase


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommentbase):

    yield serializer_ticketcommentbase

