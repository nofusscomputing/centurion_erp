import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommentactionfieldedit):

    request.cls.model = model_ticketcommentactionfieldedit

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentactionfieldedit):

    request.cls.kwargs_create_item = kwargs_ticketcommentactionfieldedit()

    yield kwargs_ticketcommentactionfieldedit


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommentactionfieldedit):

    yield serializer_ticketcommentactionfieldedit
