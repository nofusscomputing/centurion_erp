import pytest



@pytest.fixture( scope = 'class')
def model(request, model_incidentticket):

    request.cls.model = model_incidentticket

    yield request.cls.model

    del request.cls.model


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_incidentticket):

    request.cls.kwargs_create_item = kwargs_incidentticket()

    yield kwargs_incidentticket


@pytest.fixture( scope = 'class')
def model_serializer(serializer_incidentticket):

    yield serializer_incidentticket

