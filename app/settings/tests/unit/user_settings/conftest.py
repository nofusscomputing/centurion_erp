import pytest



@pytest.fixture( scope = 'class')
def model(model_usersettings):

    yield model_usersettings


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_usersettings):

    request.cls.kwargs_create_item = kwargs_usersettings.copy()

    yield kwargs_usersettings.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
