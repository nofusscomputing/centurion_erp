import pytest



@pytest.fixture( scope = 'class')
def model(request, model_requestticket):

    request.cls.model = model_requestticket

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_requestticket):

    request.cls.kwargs_create_item = kwargs_requestticket()

    yield kwargs_requestticket


@pytest.fixture( scope = 'class')
def model_serializer(serializer_requestticket):

    yield serializer_requestticket

