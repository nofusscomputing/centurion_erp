import pytest



@pytest.fixture( scope = 'class')
def model(model_clustertype):

    yield model_clustertype


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_clustertype):

    request.cls.kwargs_create_item = kwargs_clustertype.copy()

    yield kwargs_clustertype.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item


@pytest.fixture( scope = 'class')
def model_serializer(serializer_clustertype):

    yield serializer_clustertype
