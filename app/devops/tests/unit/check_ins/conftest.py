import pytest




@pytest.fixture( scope = 'class')
def model(model_checkin):

    yield model_checkin


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_checkin):

    request.cls.kwargs_create_item = kwargs_checkin.copy()

    yield kwargs_checkin.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
