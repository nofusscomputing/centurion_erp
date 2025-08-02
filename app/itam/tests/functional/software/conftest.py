import pytest



@pytest.fixture( scope = 'class')
def model(model_software):

    yield model_software


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_software):

    request.cls.kwargs_create_item = kwargs_software.copy()

    yield kwargs_software.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_software):

    yield serializer_software
