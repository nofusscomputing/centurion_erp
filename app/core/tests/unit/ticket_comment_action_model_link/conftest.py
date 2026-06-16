import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommentactionmodellink):

    request.cls.model = model_ticketcommentactionmodellink

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentactionmodellink):

    request.cls.kwargs_create_item = kwargs_ticketcommentactionmodellink()

    yield kwargs_ticketcommentactionmodellink


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommentactionmodellink):

    yield serializer_ticketcommentactionmodellink
