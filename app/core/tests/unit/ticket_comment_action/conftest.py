import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommentaction):

    request.cls.model = model_ticketcommentaction

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentaction):

    request.cls.kwargs_create_item = kwargs_ticketcommentaction.copy()

    yield kwargs_ticketcommentaction.copy()


@pytest.fixture( scope = 'class')
def model_serializer(serializer_ticketcommentaction):

    yield serializer_ticketcommentaction
