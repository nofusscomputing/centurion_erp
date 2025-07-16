import pytest



@pytest.fixture( scope = 'class')
def model(request, model_ticketcommentbase):

    request.cls.model = model_ticketcommentbase

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_ticketcommentbase):

    request.cls.kwargs_create_item = kwargs_ticketcommentbase.copy()

    yield kwargs_ticketcommentbase.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
