import pytest



@pytest.fixture( scope = 'class')
def model(model_appsettings):

    yield model_appsettings


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_appsettings):

    request.cls.kwargs_create_item = kwargs_appsettings.copy()

    yield kwargs_appsettings.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_appsettings):

    yield serializer_appsettings
