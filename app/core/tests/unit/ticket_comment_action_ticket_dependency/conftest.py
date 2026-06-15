import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommentactionticketdependency):

    request.cls.model = model_ticketcommentactionticketdependency

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentactionticketdependency):

    request.cls.kwargs_create_item = kwargs_ticketcommentactionticketdependency()

    yield kwargs_ticketcommentactionticketdependency


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommentactionticketdependency):

    yield serializer_ticketcommentactionticketdependency
