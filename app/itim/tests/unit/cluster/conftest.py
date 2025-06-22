import pytest



@pytest.fixture( scope = 'class')
def model(model_cluster):

    yield model_cluster


@pytest.fixture( scope = 'class', autouse = True)
def model_kwargs(request, kwargs_cluster):

    request.cls.kwargs_create_item = kwargs_cluster.copy()

    yield kwargs_cluster.copy()

    if hasattr(request.cls, 'kwargs_create_item'):
        del request.cls.kwargs_create_item
