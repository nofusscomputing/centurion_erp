import pytest



@pytest.fixture( scope = 'class')
def model(model_projectmilestone):

    yield model_projectmilestone


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_projectmilestone):

    request.cls.kwargs_create_item = kwargs_projectmilestone.copy()

    yield kwargs_projectmilestone.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_projectmilestone):

    yield serializer_projectmilestone
