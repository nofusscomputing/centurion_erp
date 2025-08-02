import pytest



@pytest.fixture( scope = 'class')
def model(model_operatingsystemversion):

    yield model_operatingsystemversion


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_operatingsystemversion):

    request.cls.kwargs_create_item = kwargs_operatingsystemversion.copy()

    yield kwargs_operatingsystemversion.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_operatingsystemversion):

    yield serializer_operatingsystemversion
